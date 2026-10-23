import { DIETARY_OPTIONS } from '@/constants/filters';
import { Button } from '@/components/ui/Button';
import { Tag } from '@/components/ui/Chip';
import type { Recipe, RecipeFilters } from '@/types/recipe';

const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

/** Short labels for the filters the user actually set. */
function activeFilters(filters: RecipeFilters): string[] {
  const labels = [
    filters.meal_type && capitalize(filters.meal_type),
    filters.cuisine,
    filters.difficulty && capitalize(filters.difficulty),
    filters.max_cooking_time && `≤ ${filters.max_cooking_time} min`,
    filters.servings && `Serves ${filters.servings}`,
    ...filters.dietary_preferences.map((d) => DIETARY_OPTIONS.find((o) => o.value === d)?.label ?? d),
  ];
  return labels.filter((label): label is string => Boolean(label));
}

interface ResultsScreenProps {
  recipes: Recipe[];
  ingredients: string[];
  filters: RecipeFilters;
  onSelect: (index: number) => void;
  onBack: () => void;
}

export default function ResultsScreen({ recipes, ingredients, filters, onSelect, onBack }: ResultsScreenProps) {
  const title = recipes.length === 1 ? 'A recipe for you' : `${recipes.length} recipes for you`;

  return (
    <>
      <div className="flex flex-col gap-3.5">
        <Button variant="outline" onClick={onBack} className="h-10 self-start px-3.5 text-[15px]">
          ← Edit search
        </Button>
        <h1 className="text-4xl leading-tight font-extrabold tracking-tight sm:text-5xl">{title}</h1>
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[15px] text-muted">{ingredients.join(' · ')}</span>
          {activeFilters(filters).map((label) => (
            <Tag key={label}>{label}</Tag>
          ))}
        </div>
      </div>

      <div className="grid gap-5 sm:grid-cols-[repeat(auto-fit,minmax(220px,1fr))]">
        {recipes.map((recipe, i) => (
          <button
            key={recipe.title}
            type="button"
            onClick={() => onSelect(i)}
            className="flex flex-col gap-3.5 rounded-2xl border-2 border-line bg-surface p-6 text-left transition-colors hover:border-primary"
          >
            <div className="flex gap-1.5">
              <Tag>{recipe.cooking_time} min</Tag>
              <Tag>{recipe.difficulty}</Tag>
            </div>
            <h2 className="text-2xl leading-tight font-extrabold tracking-tight">{recipe.title}</h2>
            <p className="leading-relaxed text-muted">{recipe.description}</p>
            {recipe.shopping_list.length > 0 && (
              <span className="text-sm text-muted">
                +{recipe.shopping_list.length} extra {recipe.shopping_list.length === 1 ? 'ingredient' : 'ingredients'}
              </span>
            )}
            <span className="mt-auto pt-1.5 font-extrabold text-accent-text">View recipe →</span>
          </button>
        ))}
      </div>
    </>
  );
}
