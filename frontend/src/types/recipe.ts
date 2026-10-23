export interface Recipe {
  title: string;
  description: string;
  ingredients: string[];
  instructions: string[];
  cooking_time: number;
  difficulty: string;
  servings: number;
  tags: string[];
  shopping_list: string[];
}

export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
export type Difficulty = 'easy' | 'medium' | 'hard';

/** Everything the user can choose besides the ingredients; null means "any". */
export interface RecipeFilters {
  count: number;
  meal_type: MealType | null;
  cuisine: string | null;
  difficulty: Difficulty | null;
  max_cooking_time: number | null;
  servings: number | null;
  dietary_preferences: string[];
  allow_external_ingredients: boolean;
}

export type RecipeRequest = { ingredients: string[] } & RecipeFilters;

export interface RecipeSuggestions {
  recipes: Recipe[];
}
