"""In-process asyncio broadcast bus -> SSE generator.

Every UI state transition is driven by these events, never by a POST return value
(spec: requirements.md §5, §10). Event envelope: {type, ts, msg, data?}.
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any, AsyncIterator

_KEEPALIVE_SECONDS = 15.0
_QUEUE_MAXSIZE = 200


class EventBus:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue] = set()

    async def subscribe(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=_QUEUE_MAXSIZE)
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        self._subscribers.discard(queue)

    async def publish(self, type_: str, msg: str, data: dict[str, Any] | None = None) -> dict:
        event: dict[str, Any] = {
            "type": type_,
            "ts": datetime.now(timezone.utc).isoformat(),
            "msg": msg,
        }
        if data is not None:
            event["data"] = data
        for queue in list(self._subscribers):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass  # slow consumer — drop rather than block the producer
        # Yield control so an open SSE generator can drain promptly.
        await asyncio.sleep(0)
        return event


bus = EventBus()


def format_sse(event: dict) -> str:
    return f"event: {event['type']}\ndata: {json.dumps(event)}\n\n"


async def event_stream(request) -> AsyncIterator[str]:
    """SSE generator: streams events to one subscriber until the client disconnects."""
    queue = await bus.subscribe()
    try:
        yield ": connected\n\n"
        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(queue.get(), timeout=_KEEPALIVE_SECONDS)
                yield format_sse(event)
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
    finally:
        bus.unsubscribe(queue)
