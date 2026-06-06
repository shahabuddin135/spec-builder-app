"use client";

import { useEffect, useRef, useState } from "react";
import { API_BASE } from "./api";

export interface AppEvent {
  type: string;
  ts: string;
  msg: string;
  data?: Record<string, unknown>;
}

// Named events the backend emits (CONTRACT.md > events).
const EVENT_TYPES = [
  "analysis.started",
  "analysis.done",
  "suggestions.ready",
  "spec.generated",
  "error",
];

/**
 * Subscribes to the backend SSE stream once and forwards every named event to
 * `onEvent`. UI state transitions are driven by these events, not POST returns.
 */
export function useEvents(onEvent: (ev: AppEvent) => void): { connected: boolean } {
  const [connected, setConnected] = useState(false);
  const cb = useRef(onEvent);
  cb.current = onEvent;

  useEffect(() => {
    const source = new EventSource(`${API_BASE}/events`);
    source.onopen = () => setConnected(true);
    source.onerror = () => setConnected(false);

    const handler = (e: MessageEvent) => {
      try {
        cb.current(JSON.parse(e.data) as AppEvent);
      } catch {
        /* ignore non-JSON keepalive comments */
      }
    };
    EVENT_TYPES.forEach((t) => source.addEventListener(t, handler as EventListener));

    return () => {
      EVENT_TYPES.forEach((t) =>
        source.removeEventListener(t, handler as EventListener),
      );
      source.close();
    };
  }, []);

  return { connected };
}
