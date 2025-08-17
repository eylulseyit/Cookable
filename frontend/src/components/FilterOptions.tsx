'use client';

import { FilterOptions as FilterOptionsType } from '@/types/recipe';

interface FilterOptionsProps {
  filters: FilterOptionsType & { allow_external_ingredients: boolean };
  onFiltersChange: (filters: FilterOptionsType & { allow_external_ingredients: boolean }) => void;
}

const dietaryOptions = [
  { value: 'vegetarian', label: '🥬 Vegetarian' },
  { value: 'vegan', label: '🌱 Vegan' },
  { value: 'gluten-free', label: '🌾 Gluten-Free' },
  { value: 'dairy-free', label: '🥛 Dairy-Free' },
  { value: 'low-carb', label: '🍞 Low-Carb' },
  { value: 'quick', label: '⚡ Quick (< 30 min)' },
];

const cookingTimeOptions = [
  { value: 15, label: '15 minutes' },
  { value: 30, label: '30 minutes' },
  { value: 45, label: '45 minutes' },
  { value: 60, label: '1 hour' },
  { value: 90, label: '1.5 hours' },
];

export default function FilterOptions({ filters, onFiltersChange }: FilterOptionsProps) {
  const handleDietaryPreferenceChange = (preference: string) => {
    const newPreferences = filters.dietary_preferences.includes(preference)
      ? filters.dietary_preferences.filter(p => p !== preference)
      : [...filters.dietary_preferences, preference];
    
    onFiltersChange({
      ...filters,
      dietary_preferences: newPreferences
    });
  };

  const handleCookingTimeChange = (time: number | null) => {
    onFiltersChange({
      ...filters,
      max_cooking_time: time
    });
  };

  return (
    <div className="space-y-6">
      {/* External Ingredients Toggle */}
      <div>
        <label className="flex items-center justify-between cursor-pointer">
          <span className="text-lg font-semibold text-gray-700">Suggest recipes with extra ingredients?</span>
          <div className="relative">
            <input
              type="checkbox"
              className="sr-only peer"
              checked={filters.allow_external_ingredients}
              onChange={(e) => onFiltersChange({ ...filters, allow_external_ingredients: e.target.checked })}
            />
            <div className="block bg-gray-200 peer-checked:bg-orange-500 w-14 h-8 rounded-full transition-colors"></div>
            <div className="dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform peer-checked:translate-x-6"></div>
          </div>
        </label>
        <p className="text-sm text-gray-500 mt-1">
          If enabled, we'll suggest recipes that might require a few extra items, and we'll provide a shopping list for them.
        </p>
      </div>

      {/* Dietary Preferences */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Dietary Preferences:</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {dietaryOptions.map((option) => (
            <label
              key={option.value}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={filters.dietary_preferences.includes(option.value)}
                onChange={() => handleDietaryPreferenceChange(option.value)}
                className="w-4 h-4 text-orange-600 bg-gray-100 border-gray-300 rounded focus:ring-orange-500 focus:ring-2"
              />
              <span className="text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Cooking Time */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Maximum Cooking Time:</h3>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => handleCookingTimeChange(null)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
              filters.max_cooking_time === null
                ? 'bg-orange-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            No Limit
          </button>
          {cookingTimeOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => handleCookingTimeChange(option.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                filters.max_cooking_time === option.value
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Selected Filters Summary */}
      {(filters.dietary_preferences.length > 0 || filters.max_cooking_time !== null) && (
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-orange-800 mb-2">Active Filters:</h4>
          <div className="flex flex-wrap gap-2">
            {filters.dietary_preferences.map((preference) => (
              <span
                key={preference}
                className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800"
              >
                {dietaryOptions.find(opt => opt.value === preference)?.label || preference}
              </span>
            ))}
            {filters.max_cooking_time && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                ⏱️ Max {filters.max_cooking_time} min
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 