import type { Difficulty, MealType } from '@/types/recipe';

// Choices offered in the preferences card

export const MEAL_TYPES: { value: MealType; label: string }[] = [
  { value: 'breakfast', label: 'Breakfast' },
  { value: 'lunch', label: 'Lunch' },
  { value: 'dinner', label: 'Dinner' },
  { value: 'snack', label: 'Snack' },
  { value: 'dessert', label: 'Dessert' },
];

export const CUISINES = ['Turkish', 'Italian', 'Mediterranean', 'Asian', 'Mexican', 'Indian'].map((c) => ({
  value: c,
  label: c,
}));

export const DIFFICULTIES: { value: Difficulty; label: string }[] = [
  { value: 'easy', label: 'Easy' },
  { value: 'medium', label: 'Medium' },
  { value: 'hard', label: 'Hard' },
];

export const COOKING_TIMES = [15, 30, 45, 60, 90].map((m) => ({ value: m, label: `${m} min` }));

export const DIETARY_OPTIONS = [
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'vegan', label: 'Vegan' },
  { value: 'gluten-free', label: 'Gluten-free' },
  { value: 'dairy-free', label: 'Dairy-free' },
  { value: 'low-carb', label: 'Low-carb' },
];
