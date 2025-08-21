import asyncio
import json
import os
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.services.database_service import DatabaseService
from app.core.config import settings

# --- Gemini Integration ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .vector_store_service import get_vector_store_service

# New imports for the Agent
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain import hub


_recipe_service_instance = None


def _clean_json_response(response_text: str) -> str:
    """Helper function to clean up JSON response from LLM."""
    if response_text.strip().startswith("```json"):
        response_text = response_text.strip()[7:-4].strip()
    return response_text


class RecipeService:
    def __init__(self, db: Session = None):
        self.db = db
        self.db_service = DatabaseService(db) if db else None
        
        print("--- Initializing RecipeService ---")
        if not settings.GOOGLE_API_KEY:
            print("!!! FATAL ERROR: GOOGLE_API_KEY is not being read from settings. Check your .env file and config.py.")
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        print(f"Found GOOGLE_API_KEY, starting with: '{settings.GOOGLE_API_KEY[:5]}...'")

        try:
            # Initialize the Google Gemini model
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=settings.GOOGLE_API_KEY)
            print("--- Google Gemini Model Initialized SUCCESSFULLY ---")
        except Exception as e:
            print(f"!!! FATAL ERROR: FAILED to initialize Google Gemini Model !!!")
            print(f"The error is: {e}")
            print("This usually means the API key is invalid or the 'Generative Language API' is not enabled in your Google Cloud project.")
            raise
        
        # LangChain setup for variations
        variation_template = """
        You are a helpful culinary assistant. Given the following recipe title and its ingredients, suggest three creative variations.
        For each variation, provide a new title and a brief description (1-2 sentences) of the changes.

        Original Recipe Title: {title}
        Original Ingredients: {ingredients}

        Your response MUST be a single, valid JSON object with a single key "variations", which contains a list of objects.
        Each object in the list should have two keys: "title" and "description".
        Example:
        {{
          "variations": [
            {{
              "title": "Spicy {title}",
              "description": "Add a pinch of red pepper flakes and a dash of cayenne pepper to the main sauce for a fiery kick."
            }},
            {{
              "title": "Creamy {title} Deluxe",
              "description": "Stir in a quarter cup of heavy cream at the end and top with toasted pine nuts for a richer, more decadent version."
            }}
          ]
        }}
        Do not include any text, explanation, or markdown formatting outside of the JSON object.
        """
        self.variation_prompt = PromptTemplate(template=variation_template, input_variables=["title", "ingredients"])
        self.variation_chain = LLMChain(llm=self.llm, prompt=self.variation_prompt)

        # --- Agent Tools Setup ---
        self.tools = [
            Tool(
                name="get_recipe_variations",
                func=self.get_recipe_variations,
                description="Use this tool to get creative variations for a given recipe title and its ingredients. The input should be a dictionary with 'title' and 'ingredients' keys."
            ),
            Tool(
                name="get_drink_pairing",
                func=self.get_drink_pairing,
                description="Use this tool to get drink pairing suggestions for a given recipe title. The input should be a string containing the recipe title."
            ),
            Tool(
                name="get_presentation_tips",
                func=self.get_presentation_tips,
                description="Use this tool to get tips on how to present a dish based on its title. The input should be a string containing the recipe title."
            )
        ]

        # -- Agent Setup --
        # Using a ReAct agent, which is good for reasoning and tool use.
        # The prompt is pulled from LangChain Hub to ensure it's well-tested.
        react_prompt = hub.pull("hwchase17/react")
        self.agent = create_react_agent(self.llm, self.tools, react_prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)


        self.common_ingredients = [
            "onion", "garlic", "tomato", "potato", "carrot", "bell pepper",
            "chicken", "beef", "pork", "fish", "rice", "pasta", "bread",
            "egg", "milk", "cheese", "butter", "olive oil", "salt", "pepper"
        ]
    
    def _build_recipe_prompt(
        self,
        ingredients: List[str],
        dietary_preferences: Optional[List[str]],
        max_cooking_time: Optional[int],
        allow_external_ingredients: bool,
        refinement_instruction: Optional[str] = None
    ) -> str:
        """Helper function to build the prompt for the LLM."""
        
        ingredients_str = ", ".join(ingredients)

        if refinement_instruction:
            prompt = f"""
You are a creative chef. A user wants to modify a recipe based on the instruction: "{refinement_instruction}".
The original ingredients available were: {ingredients_str}.

Please generate a new, complete recipe that incorporates this instruction. 
The new recipe should be based on the original ingredients, but you can add or remove ingredients as needed to fulfill the request.
"""
        else:
            prompt = f"""
You are a creative chef. Generate a single, delicious recipe based on the following ingredients: {ingredients_str}.
"""

        if not allow_external_ingredients and not refinement_instruction:
            prompt += "\nYou MUST ONLY use the ingredients provided. Do not suggest any extra ingredients that are not on the list."
        else:
            prompt += "\nYou can suggest a recipe that requires a few extra simple ingredients if it makes the dish significantly better. Assume the user has basic pantry staples like salt, pepper, and oil."

        prompt += "\nPlease adhere to these constraints:\n"

        if dietary_preferences:
            preferences_str = ", ".join(dietary_preferences)
            prompt += f"- Dietary Preferences: The recipe must be suitable for {preferences_str}.\\n"
        
        if max_cooking_time:
            prompt += f"- Maximum Cooking Time: The total cooking time should not exceed {max_cooking_time} minutes.\\n"

        prompt += """
Your response MUST be a single, valid JSON object with the following exact keys and value types:
- "title": (string) The name of the recipe.
- "ingredients": (list of strings) A list of all ingredients required, including quantities.
- "instructions": (list of strings) Step-by-step instructions for preparing the dish.
- "cooking_time": (integer) The total cooking time in minutes.
- "difficulty": (string) The difficulty level (e.g., "Easy", "Medium", "Hard").
- "servings": (integer) How many people the recipe serves.
- "tags": (list of strings) Relevant tags for the recipe (e.g., "vegetarian", "quick", "dinner").

Do not include any text, explanation, or markdown formatting outside of the JSON object.
"""
        return prompt.strip()

    def _build_shopping_list_prompt(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> str:
        """Helper function to build the shopping list prompt."""
        user_ingredients_str = ", ".join(user_ingredients)
        recipe_ingredients_str = ", ".join(recipe_ingredients)

        prompt = f"""
        A user has the following ingredients: {user_ingredients_str}.
        A recipe requires these ingredients: {recipe_ingredients_str}.

        Compare the two lists and generate a shopping list of ingredients the user needs to buy.
        The shopping list should only include items from the recipe that the user does not have.
        - If the user has 'chicken', and the recipe needs '1 lb boneless, skinless chicken breasts', consider it as available. General terms match specific ones.
        - Do not include quantities in the final list.
        - If the user has all the ingredients, return an empty list.

        Your response MUST be a single, valid JSON object with a single key "shopping_list" which contains a list of strings.
        Example: {{"shopping_list": ["boneless, skinless chicken breasts", "olive oil", "black pepper"]}}
        
        Do not include any text, explanation, or markdown formatting outside of the JSON object.
        """
        return prompt.strip()

    async def _generate_shopping_list(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> List[str]:
        """Generates a shopping list using the LLM."""
        if not recipe_ingredients:
            return []

        prompt = self._build_shopping_list_prompt(user_ingredients, recipe_ingredients)
        try:
            llm_response = await self.llm.ainvoke(prompt)
            response_content = llm_response.content
            
            if response_content.strip().startswith("```json"):
                response_content = response_content.strip()[7:-4].strip()

            data = json.loads(response_content)
            return data.get("shopping_list", [])
        except (json.JSONDecodeError, KeyError):
            # If parsing fails, return an empty list as a fallback
            return []

    async def get_recipe_variations(self, title: str, ingredients: List[str]) -> List[Dict[str, str]]:
        """Generates creative variations for a given recipe using LangChain."""
        try:
            formatted_ingredients = ", ".join(ingredients)
            response = await self.variation_chain.ainvoke({"title": title, "ingredients": formatted_ingredients})
            
            response_text = response['text']
            if response_text.strip().startswith("```json"):
                response_text = response_text.strip()[7:-4].strip()

            data = json.loads(response_text)
            return data.get("variations", [])
        except (json.JSONDecodeError, KeyError):
            return []

    async def get_presentation_tips(self, recipe_title: str) -> str:
        """Generates presentation tips for a given recipe."""
        prompt_template = PromptTemplate(
            template="""
            You are a food stylist. Provide three concise, actionable presentation tips for a dish called '{recipe_title}'.
            Focus on simple techniques a home cook can use.
            Your response should be a single string with tips separated by newlines.
            Example:
            - Garnish with fresh parsley before serving.
            - Serve on a contrasting colored plate to make the colors pop.
            - Wipe the rim of the plate for a clean, professional look.
            """,
            input_variables=["recipe_title"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        response = await chain.ainvoke({"recipe_title": recipe_title})
        return response['text'].strip()

    async def get_drink_pairing(self, recipe_title: str) -> str:
        """Generates drink pairing suggestions for a given recipe."""
        prompt_template = PromptTemplate(
            template="""
            You are a sommelier. Suggest one alcoholic and one non-alcoholic drink pairing for a dish called '{recipe_title}'.
            Provide a brief (1-sentence) explanation for each suggestion.
            Your response should be a single string.
            Example:
            - Alcoholic: A crisp Sauvignon Blanc. Its acidity cuts through the richness of the dish.
            - Non-Alcoholic: A sparkling lemonade with mint. It provides a refreshing contrast.
            """,
            input_variables=["recipe_title"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        response = await chain.ainvoke({"recipe_title": recipe_title})
        return response['text'].strip()
        
    async def run_gourmet_assistant_agent(self, recipe_title: str, query: str) -> str:
        """Runs the gourmet assistant agent to get suggestions based on a user query."""
        prompt = f"""
        You are the Gourmet Assistant Agent.
        The user has just received a recipe for "{recipe_title}".
        Their question or request is: "{query}"

        Based on their request, decide which of your available tools to use to provide the best answer.
        """
        try:
            response = await self.agent_executor.ainvoke({
                "input": prompt
            })
            return response.get("output", "I'm not sure how to answer that.")
        except Exception as e:
            print(f"Agent execution error: {e}")
            return "Sorry, I encountered an error while processing your request."

    async def get_recipe_recommendation(
        self, 
        ingredients: List[str], 
        dietary_preferences: Optional[List[str]] = None,
        max_cooking_time: Optional[int] = None,
        allow_external_ingredients: bool = False,
        refinement_instruction: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Recipe:
        """
        Generate a recipe recommendation based on available ingredients using Google Gemini.
        """
        if self.db_service:
            for ingredient in ingredients:
                self.db_service.increment_ingredient_popularity(ingredient)
            
            if user_id:
                self.db_service.save_user_query(
                    user_id=user_id,
                    ingredients=ingredients,
                    dietary_preferences=dietary_preferences,
                    max_cooking_time=max_cooking_time
                )
        
        # If the user is refining a previous recipe, we skip the search and go straight to the LLM.
        if refinement_instruction:
            print("--- Refinement instruction provided, skipping vector store search ---")
        else:
            # First, try to find a similar recipe in the vector store
            print("--- Searching for similar recipes in vector store ---")
            vector_store = get_vector_store_service()
            similar_recipe = vector_store.search_similar_recipes(ingredients=ingredients, similarity_threshold=1.0) # Using a high threshold for now to test
            # similar_recipe = None # Temporarily disable vector store search
            
            if similar_recipe:
                print("--- Found a similar recipe in vector store, returning it. ---")
                
                # If external ingredients are allowed, we might still need to generate a shopping list
                # for the cached recipe.
                shopping_list = await self._generate_shopping_list(
                    user_ingredients=ingredients, recipe_ingredients=similar_recipe.ingredients
                )
                similar_recipe.shopping_list = shopping_list
                
                return similar_recipe

        # If no similar recipe is found or if it's a refinement, proceed to generate a new one.
        print("--- No similar recipe found or refinement requested, generating new recipe from LLM ---")
        prompt = self._build_recipe_prompt(
            ingredients=ingredients,
            dietary_preferences=dietary_preferences,
            max_cooking_time=max_cooking_time,
            allow_external_ingredients=allow_external_ingredients,
            refinement_instruction=refinement_instruction
        )
        print("--- PROMPT SENT TO GEMINI ---")
        print(prompt)
        print("-----------------------------")
        
        try:
            # Invoke the LLM asynchronously
            llm_response = await self.llm.ainvoke(prompt)
            response_content = llm_response.content

            print("--- RAW RESPONSE FROM GEMINI ---")
            print(response_content)
            print("--------------------------------")

            # Clean up the response if it's wrapped in a markdown code block
            if response_content.strip().startswith("```json"):
                response_content = response_content.strip()[7:-4].strip()

            recipe_data = json.loads(response_content)
            
            # Create a Recipe Pydantic model instance
            recipe = Recipe(**recipe_data)

            # Add the newly generated recipe to the vector store
            vector_store = get_vector_store_service()
            vector_store.add_recipe(recipe)

            # Always generate a shopping list to see if any specific ingredients are needed
            shopping_list = await self._generate_shopping_list(
                user_ingredients=ingredients,
                recipe_ingredients=recipe.ingredients
            )
            recipe.shopping_list = shopping_list

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"!!! FAILED TO PARSE LLM RESPONSE !!!")
            print(f"Error: {e}")
            print(f"Original non-JSON response was: {response_content}")
            raise ValueError("Failed to generate a valid recipe from the AI model.")
        
        if self.db_service:
            self.db_service.create_recipe(recipe)
        
        return recipe
    
    async def get_ingredient_suggestions(self, query: str) -> List[str]:
        """
        Get ingredient suggestions based on partial input
        """
        query_lower = query.lower()
        
        # If database is available, get popular ingredients
        if self.db_service:
            popular_ingredients = self.db_service.get_popular_ingredients(10)
            suggestions = [ingredient.name for ingredient in popular_ingredients]
        else:
            suggestions = self.common_ingredients
        
        # Filter by query
        filtered_suggestions = [
            ingredient for ingredient in suggestions
            if query_lower in ingredient.lower()
        ]
        
        return filtered_suggestions[:10]  # Limit to 10 suggestions
    
    def _filter_by_dietary_preferences(
        self, 
        recipe: Recipe, 
        preferences: List[str]
    ) -> bool:
        """
        Filter recipe based on dietary preferences
        """
        if not preferences:
            return True
        
        recipe_tags = [tag.lower() for tag in recipe.tags]
        
        for preference in preferences:
            preference_lower = preference.lower()
            if preference_lower in recipe_tags:
                return True
        
        return False
    
    def _filter_by_cooking_time(
        self, 
        recipe: Recipe, 
        max_time: int
    ) -> bool:
        """
        Filter recipe based on maximum cooking time
        """
        return recipe.cooking_time <= max_time 