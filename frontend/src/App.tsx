import { useState } from 'react';
import Header from '@/components/Header';
import FormScreen from '@/screens/FormScreen';
import RecipeScreen from '@/screens/RecipeScreen';
import ResultsScreen from '@/screens/ResultsScreen';
import { ApiService } from '@/services/api';
import type { Recipe, RecipeFilters } from '@/types/recipe';

const DEFAULT_FILTERS: RecipeFilters = {
  count: 3,
  meal_type: null,
  cuisine: null,
  difficulty: null,
  max_cooking_time: null,
  servings: null,
  dietary_preferences: [],
  allow_external_ingredients: false,
};

// Which screen is shown; the recipe screen also knows which recipe
type View = { name: 'form' } | { name: 'results' } | { name: 'recipe'; index: number };

export default function App() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [filters, setFilters] = useState<RecipeFilters>(DEFAULT_FILTERS);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [view, setView] = useState<View>({ name: 'form' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const show = (next: View) => {
    setView(next);
    window.scrollTo({ top: 0 });
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await ApiService.getRecipeSuggestions({ ingredients, ...filters });
      setRecipes(result);
      // A single recipe skips the results list
      show(result.length === 1 ? { name: 'recipe', index: 0 } : { name: 'results' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Header />
      <main className="mx-auto flex max-w-3xl flex-col gap-6 px-4 pt-8 pb-20 sm:px-6">
        {view.name === 'form' && (
          <FormScreen
            ingredients={ingredients}
            filters={filters}
            loading={loading}
            error={error}
            onIngredientsChange={setIngredients}
            onFiltersChange={setFilters}
            onSubmit={handleSubmit}
          />
        )}
        {view.name === 'results' && (
          <ResultsScreen
            recipes={recipes}
            ingredients={ingredients}
            filters={filters}
            onSelect={(index) => show({ name: 'recipe', index })}
            onBack={() => show({ name: 'form' })}
          />
        )}
        {view.name === 'recipe' && (
          <RecipeScreen
            recipes={recipes}
            index={view.index}
            onSelect={(index) => show({ name: 'recipe', index })}
            onBack={() => show(recipes.length > 1 ? { name: 'results' } : { name: 'form' })}
          />
        )}
      </main>
    </div>
  );
}
