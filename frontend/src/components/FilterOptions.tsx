import { Card, StepHeading } from '@/components/ui/Card';
import { ToggleChip } from '@/components/ui/Chip';
import { SelectField } from '@/components/ui/SelectField';
import { Stepper } from '@/components/ui/Stepper';
import { COOKING_TIMES, CUISINES, DIETARY_OPTIONS, DIFFICULTIES, MEAL_TYPES } from '@/constants/filters';
import type { RecipeFilters } from '@/types/recipe';

interface FilterOptionsProps {
  filters: RecipeFilters;
  onFiltersChange: (filters: RecipeFilters) => void;
}

export default function FilterOptions({ filters, onFiltersChange }: FilterOptionsProps) {
  const update = (changes: Partial<RecipeFilters>) => onFiltersChange({ ...filters, ...changes });

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
      <StepHeading step={2} title="Preferences" hint="all optional" />

      <div className="grid grid-cols-[repeat(auto-fit,minmax(150px,1fr))] gap-4">
        <SelectField label="Meal" value={filters.meal_type} options={MEAL_TYPES} onChange={(meal_type) => update({ meal_type })} />
        <SelectField label="Cuisine" value={filters.cuisine} options={CUISINES} onChange={(cuisine) => update({ cuisine })} />
        <SelectField label="Difficulty" value={filters.difficulty} options={DIFFICULTIES} onChange={(difficulty) => update({ difficulty })} />
        <SelectField label="Max time" value={filters.max_cooking_time} options={COOKING_TIMES} onChange={(max_cooking_time) => update({ max_cooking_time })} />
        <Stepper label="Servings" value={filters.servings} min={1} max={12} onChange={(servings) => update({ servings })} />
      </div>

      <div className="flex flex-col gap-2.5">
        <span className="text-sm text-muted">Diet</span>
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
      </div>

      <label className="flex items-center gap-2.5 text-[15px]">
        <input
          type="checkbox"
          checked={filters.allow_external_ingredients}
          onChange={(e) => update({ allow_external_ingredients: e.target.checked })}
          className="size-5 accent-primary"
        />
        Allow a few extras
        <span className="text-sm text-muted">(adds a shopping list)</span>
      </label>
    </Card>
  );
}
