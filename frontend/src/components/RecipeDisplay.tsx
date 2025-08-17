'use client';

import { Recipe } from '@/types/recipe';

interface RecipeDisplayProps {
  recipe: Recipe;
}

export default function RecipeDisplay({ recipe }: RecipeDisplayProps) {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Recipe Header */}
      <div className="text-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-2">{recipe.title}</h3>
        <div className="flex justify-center items-center gap-4 text-sm text-gray-600">
          <span className="flex items-center gap-1">
            ⏱️ {recipe.cooking_time} minutes
          </span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
            {recipe.difficulty}
          </span>
          <span className="flex items-center gap-1">
            👥 {recipe.servings} servings
          </span>
        </div>
      </div>

      {/* Recipe Tags */}
      {recipe.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 justify-center">
          {recipe.tags.map((tag, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Ingredients */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          🥘 Ingredients
        </h4>
        <ul className="space-y-2">
          {recipe.ingredients.map((ingredient, index) => (
            <li
              key={index}
              className="flex items-start gap-3 text-gray-700"
            >
              <span className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></span>
              <span>{ingredient}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Instructions */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          📝 Instructions
        </h4>
        <ol className="space-y-4">
          {recipe.instructions.map((instruction, index) => (
            <li
              key={index}
              className="flex gap-4 text-gray-700"
            >
              <span className="flex-shrink-0 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                {index + 1}
              </span>
              <span className="flex-1">{instruction}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Shopping List */}
      {recipe.shopping_list && recipe.shopping_list.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h4 className="text-xl font-semibold text-blue-800 mb-4 flex items-center gap-2">
            🛒 Shopping List
          </h4>
          <ul className="space-y-2">
            {recipe.shopping_list.map((item, index) => (
              <li
                key={index}
                className="flex items-start gap-3 text-gray-700"
              >
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recipe Summary */}
      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
        <h4 className="text-lg font-semibold text-orange-800 mb-2">Recipe Summary</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{recipe.cooking_time}</div>
            <div className="text-gray-600">Minutes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{recipe.servings}</div>
            <div className="text-gray-600">Servings</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{recipe.ingredients.length}</div>
            <div className="text-gray-600">Ingredients</div>
          </div>
        </div>
      </div>
    </div>
  );
} 