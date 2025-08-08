from app.core.database import engine, Base
from app.models.database_models import *  # Import all models
from app.services.database_service import DatabaseService
from app.core.database import SessionLocal

def init_db():
    """Initialize the database with tables and sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Add sample data
    print("Adding sample data...")
    db = SessionLocal()
    try:
        db_service = DatabaseService(db)
        
        # Add sample ingredients
        sample_ingredients = [
            "onion", "garlic", "tomato", "potato", "carrot", "bell pepper",
            "chicken", "beef", "pork", "fish", "rice", "pasta", "bread",
            "egg", "milk", "cheese", "butter", "olive oil", "salt", "pepper"
        ]
        
        for ingredient_name in sample_ingredients:
            db_service.get_or_create_ingredient(ingredient_name)
        
        # Add sample tags
        sample_tags = [
            "vegetarian", "vegan", "gluten-free", "dairy-free", "quick",
            "pasta", "soup", "salad", "dessert", "breakfast"
        ]
        
        for tag_name in sample_tags:
            db_service.get_or_create_tag(tag_name)
        
        print("✅ Sample data added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 