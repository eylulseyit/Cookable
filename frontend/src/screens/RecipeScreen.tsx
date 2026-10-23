import RecipeDisplay from '@/components/RecipeDisplay';
import { Button } from '@/components/ui/Button';
import type { Recipe } from '@/types/recipe';

interface RecipeScreenProps {
  recipes: Recipe[];
  index: number;
  onSelect: (index: number) => void;
  onBack: () => void;
}

export default function RecipeScreen({ recipes, index, onSelect, onBack }: RecipeScreenProps) {
  const others = recipes.map((recipe, i) => ({ recipe, i })).filter(({ i }) => i !== index);

  return (
    <>
      <Button variant="outline" onClick={onBack} className="h-10 self-start px-3.5 text-[15px]">
        {recipes.length > 1 ? `← All ${recipes.length} recipes` : '← Edit search'}
      </Button>

      <RecipeDisplay recipe={recipes[index]} />

      {others.length > 0 && (
        <div className="flex flex-col gap-3">
          <span className="text-sm text-muted">Other suggestions</span>
          <div className="flex flex-wrap gap-2.5">
            {others.map(({ recipe, i }) => (
              <button
                key={recipe.title}
                type="button"
                onClick={() => onSelect(i)}
                className="flex h-12 items-center gap-2.5 rounded-xl border-2 border-line bg-surface px-4.5 text-[15px] font-semibold transition-colors hover:border-primary"
              >
                {recipe.title}
                <span className="font-medium text-muted">{recipe.cooking_time} min</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
