import type { ReactNode } from 'react';

interface ToggleChipProps {
  children: ReactNode;
  selected: boolean;
  onClick: () => void;
}

/** A pill that can be switched on and off, e.g. a filter. */
export function ToggleChip({ children, selected, onClick }: ToggleChipProps) {
  const look = selected
    ? 'border-selected bg-selected text-on-selected font-semibold'
    : 'border-field-line bg-field text-fg';
  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={onClick}
      className={`h-10 rounded-[10px] border-2 px-4 text-[15px] transition-colors ${look}`}
    >
      {children}
    </button>
  );
}

interface RemovableChipProps {
  label: string;
  onRemove: () => void;
}

/** A selected item with a remove button, e.g. an added ingredient. */
export function RemovableChip({ label, onRemove }: RemovableChipProps) {
  return (
    <span className="inline-flex h-[38px] items-center gap-1.5 rounded-[10px] bg-primary pr-1.5 pl-3.5 text-[15px] font-semibold text-on-primary">
      {label}
      <button
        type="button"
        onClick={onRemove}
        aria-label={`Remove ${label}`}
        className="flex size-7 items-center justify-center rounded-lg text-lg leading-none hover:bg-black/10"
      >
        ×
      </button>
    </span>
  );
}

interface TagProps {
  children: ReactNode;
  accent?: boolean;
}

/** A small read-only label, e.g. a recipe's cooking time. */
export function Tag({ children, accent = false }: TagProps) {
  const look = accent ? 'bg-primary text-on-primary' : 'bg-tag text-on-tag';
  return <span className={`rounded-lg px-3 py-1.5 text-sm font-semibold ${look}`}>{children}</span>;
}
