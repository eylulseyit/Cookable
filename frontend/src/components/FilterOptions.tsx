import { Card, StepHeading } from '@/components/ui/Card';
import { ToggleChip } from '@/components/ui/Chip';
import { fieldClass } from '@/components/ui/field';
import type { FilterOptions as Filters } from '@/types/recipe';

const DIETARY_OPTIONS = [
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'vegan', label: 'Vegan' },
  { value: 'gluten-free', label: 'Gluten-free' },
  { value: 'dairy-free', label: 'Dairy-free' },
  { value: 'low-carb', label: 'Low-carb' },
];

const COOKING_TIMES = [15, 30, 45, 60, 90];

interface FilterOptionsProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}

export default function FilterOptions({ filters, onFiltersChange }: FilterOptionsProps) {
  const update = (changes: Partial<Filters>) => onFiltersChange({ ...filters, ...changes });

  const togglePreference = (preference: string) => {
    const current = filters.dietary_preferences;
    update({
      dietary_preferences: current.includes(preference)
        ? current.filter((p) => p !== preference)
        : [...current, preference],
    });
  };

  return (
    <Card>
      <StepHeading step={2} title="Filters" hint="optional" />

      <div className="flex flex-wrap gap-2">
        {DIETARY_OPTIONS.map(({ value, label }) => (
          <ToggleChip
            key={value}
            selected={filters.dietary_preferences.includes(value)}
            onClick={() => togglePreference(value)}
          >
            {label}
          </ToggleChip>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-6 text-[15px]">
        <label className="flex items-center gap-2.5">
          Max time
          <select
            value={filters.max_cooking_time ?? ''}
            onChange={(e) => update({ max_cooking_time: e.target.value ? Number(e.target.value) : null })}
            className={`h-10 px-3 ${fieldClass}`}
          >
            <option value="">Any</option>
            {COOKING_TIMES.map((minutes) => (
              <option key={minutes} value={minutes}>{minutes} min</option>
            ))}
          </select>
        </label>

        <label className="flex items-center gap-2.5">
          <input
            type="checkbox"
            checked={filters.allow_external_ingredients}
            onChange={(e) => update({ allow_external_ingredients: e.target.checked })}
            className="size-5 accent-primary"
          />
          Allow a few extras
          <span className="text-sm text-muted">(adds a shopping list)</span>
        </label>
      </div>
    </Card>
  );
}
