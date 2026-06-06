"use client";

export function TopNav({ onStartOver }: { onStartOver?: () => void }) {
  return (
    <nav className="fixed top-0 z-50 flex h-12 w-full items-center border-b border-outline bg-surface-container-low px-6 sm:px-10">
      <div className="flex flex-1 items-center">
        {onStartOver && (
          <button
            onClick={onStartOver}
            className="flex cursor-pointer items-center gap-1 text-on-surface-variant transition-colors hover:text-primary active:opacity-80"
          >
            <span className="material-symbols-outlined text-[20px]">arrow_back</span>
            <span className="text-label-md">Start over</span>
          </button>
        )}
      </div>
      <div className="flex flex-none items-center gap-1.5">
        <span className="material-symbols-outlined text-[22px] text-primary">terminal</span>
        <span className="text-headline-md font-bold tracking-tight text-primary">
          SpecForge
        </span>
      </div>
      <div className="flex-1" />
    </nav>
  );
}
