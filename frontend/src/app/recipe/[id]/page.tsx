import { Recipe } from '@/types/recipe';
import { notFound } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { GourmetAssistant } from '@/components/GourmetAssistant';

async function getRecipe(id: string): Promise<Recipe | null> {
  try {
    const res = await fetch(`${process.env.NEXT_URL}/api/recipes/${id}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!res.ok) {
      throw new Error('Failed to fetch recipe');
    }

    const recipe = await res.json();
    return recipe;
  } catch (error) {
    console.error('Error fetching recipe:', error);
    return null;
  }
}

export default async function RecipePage({ params }: { params: { id: string } }) {
  const recipe = await getRecipe(params.id);

  if (!recipe) {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-zinc-900 mb-2">{recipe.title}</h1>
        <p className="text-lg text-zinc-700">{recipe.description}</p>
        <div className="flex items-center justify-center mt-4 text-zinc-600 text-sm">
          <span>{recipe.cookingTime} min</span>
          <span className="mx-2">•</span>
          <span>{recipe.servings} servings</span>
        </div>
      </div>

      {/* Agent Assistant Section */}
      <GourmetAssistant recipeTitle={recipe.title} />

      {/* Main Content */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
        {/* Ingredients */}
        <div className="md:col-span-1">
          <h2 className="text-2xl font-bold text-zinc-900 mb-4">Ingredients</h2>
          <ul className="list-disc list-inside text-zinc-800">
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
        </div>

        {/* Instructions */}
        <div className="md:col-span-2">
          <h2 className="text-2xl font-bold text-zinc-900 mb-4">Instructions</h2>
          <ol className="list-decimal list-inside text-zinc-800">
            {recipe.instructions.map((instruction, index) => (
              <li key={index} className="mb-4 last:mb-0">
                <p className="text-lg text-zinc-900 font-semibold mb-2">{instruction.step}</p>
                <p className="text-zinc-700">{instruction.description}</p>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
}
