# Database Setup Guide

## PostgreSQL Installation

### Option 1: Install PostgreSQL Locally
1. Download PostgreSQL from: https://www.postgresql.org/download/
2. Install with default settings
3. Remember the password you set for the `postgres` user

### Option 2: Use Docker (Recommended)
```bash
# Run PostgreSQL in Docker
docker run --name recipe-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=recipe_db -p 5432:5432 -d postgres:15
```

## Database Configuration

1. Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/recipe_db
API_V1_STR=/api/v1
PROJECT_NAME=Recipe Recommendation API
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

2. Initialize the database:
```bash
cd backend
python init_db.py
```

## Database Schema

The application creates the following tables:

- **users** - User accounts for tracking queries
- **ingredients** - Available ingredients with popularity tracking
- **tags** - Recipe tags (vegetarian, quick, etc.)
- **recipes** - Generated recipes
- **recipe_instructions** - Step-by-step instructions
- **user_queries** - Track user search queries
- **recipe_ratings** - User ratings and feedback

## Features Added

✅ **Recipe Storage** - Save generated recipes to database
✅ **Ingredient Tracking** - Track popular ingredients
✅ **User Analytics** - Save user queries for insights
✅ **Query History** - Track what users search for
✅ **Popular Ingredients** - Show trending ingredients

## Testing the Database

1. Start the backend server:
```bash
uvicorn main:app --reload
```

2. Test the API endpoints:
- `POST /api/v1/users/create` - Create a user
- `POST /api/v1/recipes/recommend` - Get recipe (saves to DB)
- `GET /api/v1/ingredients/popular` - Get popular ingredients
- `GET /api/v1/ingredients/suggestions?query=onion` - Get suggestions

## Next Steps

After database setup, you can:
1. Add AI integration for real recipe generation
2. Implement user authentication
3. Add recipe rating system
4. Create analytics dashboard 