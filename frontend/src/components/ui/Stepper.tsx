interface StepperProps {
  label: string;
  value: number | null;
  min: number;
  max: number;
  onChange: (value: number | null) => void;
}

/** A number picker with - and +; going below `min` means "any" (null). */
export function Stepper({ label, value, min, max, onChange }: StepperProps) {
  const decrease = () => onChange(value === null || value <= min ? null : value - 1);
  const increase = () => onChange(value === null ? min : Math.min(value + 1, max));
  const buttonClass = 'h-full w-11 text-xl disabled:opacity-40';

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm text-muted">{label}</span>
      <div className="flex h-11 items-center overflow-hidden rounded-xl border-2 border-field-line bg-field">
        <button type="button" onClick={decrease} disabled={value === null} aria-label={`Fewer ${label.toLowerCase()}`} className={buttonClass}>
          −
        </button>
        <span aria-live="polite" className="flex-1 text-center font-bold">{value ?? 'Any'}</span>
        <button type="button" onClick={increase} disabled={value === max} aria-label={`More ${label.toLowerCase()}`} className={buttonClass}>
          +
        </button>
      </div>
    </div>
  );
}
