import { fieldClass } from '@/components/ui/field';

interface SelectFieldProps<T extends string | number> {
  label: string;
  value: T | null;
  options: { value: T; label: string }[];
  onChange: (value: T | null) => void;
}

/** A labelled select whose first option, "Any", stands for null. */
export function SelectField<T extends string | number>({ label, value, options, onChange }: SelectFieldProps<T>) {
  return (
    <label className="flex flex-col gap-2 text-sm text-muted">
      {label}
      <select
        value={value ?? ''}
        onChange={(e) => {
          const option = options.find((o) => String(o.value) === e.target.value);
          onChange(option ? option.value : null);
        }}
        className={`h-11 px-3 text-[15px] ${fieldClass}`}
      >
        <option value="">Any</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </label>
  );
}
