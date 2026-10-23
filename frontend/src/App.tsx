import { useState } from 'react';
import FilterOptions from '@/components/FilterOptions';
import IngredientInput from '@/components/IngredientInput';
import RecipeDisplay from '@/components/RecipeDisplay';
import ThemeToggle from '@/components/ThemeToggle';
import { Button } from '@/components/ui/Button';
import { ApiService } from '@/services/api';
import type { FilterOptions as Filters, Recipe } from '@/types/recipe';

const DEFAULT_FILTERS: Filters = {
  dietary_preferences: [],
  max_cooking_time: null,
  allow_external_ingredients: false,
};

export default function App() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS);
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGetRecipe = async () => {
    if (ingredients.length === 0) {
      setError('Please enter at least one ingredient');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const recipeData = await ApiService.getRecipeRecommendation({
        ingredients,
        dietary_preferences: filters.dietary_preferences.length > 0 ? filters.dietary_preferences : undefined,
        max_cooking_time: filters.max_cooking_time ?? undefined,
        allow_external_ingredients: filters.allow_external_ingredients,
      });
      setRecipe(recipeData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setIngredients([]);
    setFilters(DEFAULT_FILTERS);
    setRecipe(null);
    setError(null);
  };

  return (
    <div className="min-h-screen px-4 pt-14 pb-20 sm:px-6">
      <main className="mx-auto flex max-w-3xl flex-col gap-6">
        <header className="flex items-start justify-between gap-4 pb-5">
          <div className="flex flex-col gap-3.5">
            <h1 className="text-6xl leading-none font-extrabold tracking-tighter sm:text-7xl">
              Cook<span className="text-accent">able</span>
            </h1>
            <p className="text-lg text-muted">Your ingredients in. A recipe out.</p>
          </div>
          <ThemeToggle />
        </header>

        <IngredientInput ingredients={ingredients} onIngredientsChange={setIngredients} />
        <FilterOptions filters={filters} onFiltersChange={setFilters} />

        <Button
          variant="primary"
          onClick={handleGetRecipe}
          disabled={loading || ingredients.length === 0}
          className="h-16 text-xl tracking-tight"
        >
          {loading ? 'Cooking up a recipe...' : 'Get my recipe →'}
        </Button>

        {error && (
          <div role="alert" className="rounded-xl border-2 border-danger bg-surface px-4 py-3 font-medium text-danger">
            {error}
          </div>
        )}

        {recipe && (
          <>
            <RecipeDisplay recipe={recipe} />
            <Button variant="outline" onClick={handleReset} className="h-12 self-center px-6">
              Start over
            </Button>
          </>
        )}
      </main>
    </div>
  );
}
