import FilterOptions from '@/components/FilterOptions';
import IngredientInput from '@/components/IngredientInput';
import { Button } from '@/components/ui/Button';
import { Segmented } from '@/components/ui/Segmented';
import type { RecipeFilters } from '@/types/recipe';

interface FormScreenProps {
  ingredients: string[];
  filters: RecipeFilters;
  loading: boolean;
  error: string | null;
  onIngredientsChange: (ingredients: string[]) => void;
  onFiltersChange: (filters: RecipeFilters) => void;
  onSubmit: () => void;
}

export default function FormScreen({
  ingredients,
  filters,
  loading,
  error,
  onIngredientsChange,
  onFiltersChange,
  onSubmit,
}: FormScreenProps) {
  const { count } = filters;

  return (
    <>
      <IngredientInput ingredients={ingredients} onIngredientsChange={onIngredientsChange} />
      <FilterOptions filters={filters} onFiltersChange={onFiltersChange} />

      <div className="flex flex-wrap items-center gap-4 rounded-2xl border-2 border-primary bg-surface py-4 pr-4 pl-6">
        <span className="text-[15px] font-semibold">How many recipes?</span>
        <Segmented
          label="Number of recipes"
          value={count}
          options={[1, 2, 3, 4, 5]}
          onChange={(value) => onFiltersChange({ ...filters, count: value })}
        />
        <Button
          variant="primary"
          onClick={onSubmit}
          disabled={loading || ingredients.length === 0}
          className="ml-auto h-14 px-7 text-lg tracking-tight"
        >
          {loading ? `Cooking up ${count === 1 ? 'a recipe' : `${count} recipes`}...` : `Get ${count === 1 ? 'a recipe' : `${count} recipes`} →`}
        </Button>
      </div>

      {error && (
        <div role="alert" className="rounded-xl border-2 border-danger bg-surface px-4 py-3 font-medium text-danger">
          {error}
        </div>
      )}
    </>
  );
}
