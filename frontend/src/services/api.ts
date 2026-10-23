import { Recipe, IngredientRequest } from '@/types/recipe';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function errorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    // FastAPI returns a string for HTTPException and a list for validation errors
    if (typeof data.detail === 'string') return data.detail;
  } catch {
    // Response body was not JSON
  }
  return `Request failed (${response.status})`;
}

export class ApiService {
  static async getRecipeRecommendation(request: IngredientRequest): Promise<Recipe> {
    let response: Response;
    try {
      response = await fetch(`${API_BASE_URL}/recipes/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
    } catch {
      throw new Error('Could not reach the Cookable API. Is the backend running?');
    }

    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    return response.json();
  }

  static async getIngredientSuggestions(query: string): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/ingredients/suggestions?query=${encodeURIComponent(query)}`);

    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    const data = await response.json();
    return data.suggestions || [];
  }

  static async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/recipes/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}
