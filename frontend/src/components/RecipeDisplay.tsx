import { Card } from '@/components/ui/Card';
import { Tag } from '@/components/ui/Chip';
import type { Recipe } from '@/types/recipe';

interface RecipeDisplayProps {
  recipe: Recipe;
}

export default function RecipeDisplay({ recipe }: RecipeDisplayProps) {
  const shoppingList = recipe.shopping_list ?? [];

  return (
    <Card highlight className="gap-6 sm:p-8">
      <div className="flex flex-col gap-3">
        <h2 className="text-4xl leading-tight font-extrabold tracking-tight">{recipe.title}</h2>
        <div className="flex flex-wrap gap-2">
          <Tag>{recipe.cooking_time} min</Tag>
          <Tag>{recipe.difficulty}</Tag>
          <Tag>Serves {recipe.servings}</Tag>
          {recipe.tags.map((tag) => (
            <Tag key={tag} accent>{tag}</Tag>
          ))}
        </div>
      </div>

      <div className="grid gap-8 sm:grid-cols-2">
        <div className="flex flex-col gap-3">
          <h3 className="text-lg font-extrabold">Ingredients</h3>
          <ul className="list-disc space-y-2 pl-5 leading-relaxed">
            {recipe.ingredients.map((ingredient, i) => (
              <li key={i}>{ingredient}</li>
            ))}
          </ul>
        </div>
        <div className="flex flex-col gap-3">
          <h3 className="text-lg font-extrabold">Steps</h3>
          <ol className="list-decimal space-y-2 pl-5 leading-relaxed">
            {recipe.instructions.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
      </div>

      {shoppingList.length > 0 && (
        <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 rounded-xl bg-primary px-5 py-4 text-[15px] text-on-primary">
          <span className="font-extrabold">Shopping list</span>
          <span>{shoppingList.join(', ')}</span>
        </div>
      )}
    </Card>
  );
}
