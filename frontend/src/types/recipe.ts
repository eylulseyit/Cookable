export interface Recipe {
  title: string;
  ingredients: string[];
  instructions: string[];
  cooking_time: number;
  difficulty: string;
  servings: number;
  tags: string[];
  shopping_list?: string[];
}

export interface IngredientRequest {
  ingredients: string[];
  dietary_preferences?: string[];
  max_cooking_time?: number;
  allow_external_ingredients?: boolean;
}

export interface FilterOptions {
  dietary_preferences: string[];
  max_cooking_time: number | null;
  allow_external_ingredients: boolean;
}
