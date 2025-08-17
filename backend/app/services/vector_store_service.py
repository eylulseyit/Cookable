import chromadb
from chromadb.utils import embedding_functions
import json
from ..models.recipe import Recipe
from ..core.config import settings
from pathlib import Path

class VectorStoreService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            db_path = Path(settings.CHROMA_DB_PATH)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            cls._instance.client = chromadb.PersistentClient(path=str(db_path))
            
            cls._instance.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.EMBEDDING_MODEL_NAME
            )
            
            cls._instance.collection = cls._instance.client.get_or_create_collection(
                name="recipes",
                embedding_function=cls._instance.sentence_transformer_ef
            )
            print("--- ChromaDB Collection Initialized ---")
        return cls._instance

    def _recipe_to_document(self, recipe: Recipe) -> str:
        """Converts a Recipe object into a string document for embedding."""
        tags = ", ".join(recipe.tags) if recipe.tags else "No tags"
        ingredients = ", ".join(recipe.ingredients)
        document = f"Title: {recipe.title}. Ingredients: {ingredients}. Tags: {tags}. Difficulty: {recipe.difficulty}."
        return document

    def add_recipe(self, recipe: Recipe):
        """Adds a recipe to the vector store."""
        document = self._recipe_to_document(recipe)
        metadata = recipe.model_dump()
        
        # ChromaDB metadata values must be JSON-serializable and cannot be lists or None.
        # We'll convert lists to JSON strings and skip None values.
        serializable_metadata = {}
        for key, value in metadata.items():
            if value is None:
                continue # Skip fields with None value
            if isinstance(value, list):
                serializable_metadata[key] = json.dumps(value)
            elif isinstance(value, (str, int, float, bool)):
                serializable_metadata[key] = value
            else:
                serializable_metadata[key] = str(value)

        # ChromaDB requires a unique ID for each document. We can create one based on the title.
        # A more robust solution might use a UUID or a hash of the content.
        recipe_id = recipe.title.lower().replace(" ", "-").strip()

        try:
            self.collection.add(
                documents=[document],
                metadatas=[serializable_metadata],
                ids=[recipe_id]
            )
            print(f"--- Recipe '{recipe.title}' added to Vector Store ---")
        except Exception as e:
            print(f"Error adding recipe to ChromaDB: {e}")

    def search_similar_recipes(self, ingredients: list[str], n_results: int = 1, similarity_threshold: float = 1.0) -> Recipe | None:
        """Searches for recipes with similar ingredients."""
        if not ingredients:
            return None

        query_document = f"Recipe with ingredients: {', '.join(ingredients)}"
        
        try:
            results = self.collection.query(
                query_texts=[query_document],
                n_results=n_results
            )
            
            # Check for valid results and that the lists inside are not empty
            if not results or not results["distances"] or not results["metadatas"] or not results["distances"][0]:
                print("--- No similar recipes found in Vector Store ---")
                return None

            # Chroma returns distances, not similarity scores. A lower distance means higher similarity.
            # For SentenceTransformers with cosine similarity, distance is 1 - similarity.
            # A lower distance is better. We'll use a threshold to filter.
            
            distance = results["distances"][0][0]
            
            print(f"--- Found closest recipe with distance: {distance} ---")

            if distance < similarity_threshold:
                print("--- Similar recipe found above threshold ---")
                metadata_from_db = results["metadatas"][0][0]
                
                # De-serialize list-like fields from JSON strings back to lists
                for key, value in metadata_from_db.items():
                    if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                        try:
                            metadata_from_db[key] = json.loads(value)
                        except json.JSONDecodeError:
                            pass # Keep it as a string if it's not valid JSON

                return Recipe(**metadata_from_db)
            else:
                print("--- Closest recipe below similarity threshold ---")
                return None

        except Exception as e:
            print(f"Error searching for similar recipes in ChromaDB: {e}")
            return None


def get_vector_store_service():
    return VectorStoreService()
