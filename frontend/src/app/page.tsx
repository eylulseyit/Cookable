'use client';

import { useState } from 'react';
import IngredientInput from '@/components/IngredientInput';
import RecipeDisplay from '@/components/RecipeDisplay';
import FilterOptions from '@/components/FilterOptions';
import { Recipe } from '@/types/recipe';

export default function Home() {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [filters, setFilters] = useState({
    dietary_preferences: [] as string[],
    max_cooking_time: null as number | null,
    allow_external_ingredients: false
  });
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
      const response = await fetch('http://localhost:8000/api/v1/recipes/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ingredients,
          dietary_preferences: filters.dietary_preferences.length > 0 ? filters.dietary_preferences : undefined,
          max_cooking_time: filters.max_cooking_time || undefined,
          allow_external_ingredients: filters.allow_external_ingredients,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get recipe recommendation');
      }

      const recipeData = await response.json();
      setRecipe(recipeData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setIngredients([]);
    setFilters({
      dietary_preferences: [],
      max_cooking_time: null,
      allow_external_ingredients: false
    });
    setRecipe(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🍳 Recipe Recommender
          </h1>
          <p className="text-gray-600 text-lg">
            Enter your available ingredients and get AI-powered recipe suggestions
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Step 1: Ingredient Input */}
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              1️⃣ Enter Your Ingredients
            </h2>
            <IngredientInput
              ingredients={ingredients}
              onIngredientsChange={setIngredients}
            />
          </div>

          {/* Step 2: Filter Options */}
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              2️⃣ Optional Filters
            </h2>
            <FilterOptions
              filters={filters}
              onFiltersChange={setFilters}
            />
          </div>

          {/* Step 3: Get Recipe Button */}
          <div className="text-center mb-6">
            <button
              onClick={handleGetRecipe}
              disabled={loading || ingredients.length === 0}
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors duration-200"
            >
              {loading ? '🍳 Cooking up a recipe...' : '🍽️ Get Recipe Recommendation'}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {/* Step 4: Recipe Display */}
          {recipe && (
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                3️⃣ Your Recipe
              </h2>
              <RecipeDisplay recipe={recipe} />
            </div>
          )}

          {/* Reset Button */}
          {recipe && (
            <div className="text-center">
              <button
                onClick={handleReset}
                className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-lg transition-colors duration-200"
              >
                🔄 Start Over
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
