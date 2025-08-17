'use client';

import { useState } from 'react';

interface IngredientInputProps {
  ingredients: string[];
  onIngredientsChange: (ingredients: string[]) => void;
}

export default function IngredientInput({ ingredients, onIngredientsChange }: IngredientInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleAddIngredient = () => {
    const trimmedValue = inputValue.trim();
    if (trimmedValue && !ingredients.includes(trimmedValue.toLowerCase())) {
      onIngredientsChange([...ingredients, trimmedValue.toLowerCase()]);
      setInputValue('');
    }
  };

  const handleRemoveIngredient = (index: number) => {
    const newIngredients = ingredients.filter((_, i) => i !== index);
    onIngredientsChange(newIngredients);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddIngredient();
    }
  };

  return (
    <div className="space-y-4">
      {/* Input Field */}
      <div className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter an ingredient (e.g., chicken, tomato, rice)"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
        <button
          onClick={handleAddIngredient}
          disabled={!inputValue.trim()}
          className="px-6 py-2 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200"
        >
          Add
        </button>
      </div>

      {/* Ingredients List */}
      {ingredients.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Your Ingredients:</h3>
          <div className="flex flex-wrap gap-2">
            {ingredients.map((ingredient, index) => (
              <div
                key={index}
                className="flex items-center gap-2 bg-orange-100 text-orange-800 px-3 py-1 rounded-full"
              >
                <span className="text-sm font-medium">{ingredient}</span>
                <button
                  onClick={() => handleRemoveIngredient(index)}
                  className="text-orange-600 hover:text-orange-800 text-lg font-bold"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Add Suggestions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Quick Add Common Ingredients:</h3>
        <div className="flex flex-wrap gap-2">
          {['onion', 'garlic', 'tomato', 'chicken', 'rice', 'pasta', 'egg', 'cheese'].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => {
                if (!ingredients.includes(suggestion)) {
                  onIngredientsChange([...ingredients, suggestion]);
                }
              }}
              disabled={ingredients.includes(suggestion)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 text-gray-700 rounded-full text-sm transition-colors duration-200"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
} 