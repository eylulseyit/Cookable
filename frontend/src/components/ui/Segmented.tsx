interface SegmentedProps {
  label: string;
  value: number;
  options: number[];
  onChange: (value: number) => void;
}

/** A row of mutually exclusive number buttons, e.g. 1 to 5. */
export function Segmented({ label, value, options, onChange }: SegmentedProps) {
  return (
    <div role="group" aria-label={label} className="flex gap-1 rounded-xl bg-field p-1">
      {options.map((option) => {
        const selected = option === value;
        return (
          <button
            key={option}
            type="button"
            aria-pressed={selected}
            onClick={() => onChange(option)}
            className={`h-10 w-11 rounded-[9px] font-extrabold transition-colors ${
              selected ? 'bg-primary text-on-primary' : 'text-fg'
            }`}
          >
            {option}
          </button>
        );
      })}
    </div>
  );
}
