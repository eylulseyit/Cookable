import { Recipe, IngredientRequest } from '@/types/recipe';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export class ApiService {
  static async getRecipeRecommendation(request: IngredientRequest): Promise<Recipe> {
    const response = await fetch(`${API_BASE_URL}/recipes/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  static async getIngredientSuggestions(query: string): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/ingredients/suggestions?query=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.suggestions || [];
  }

  static async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/recipes/health`, {
        method: 'GET',
      });
      return response.ok;
    } catch {
      return false;
    }
  }
} 