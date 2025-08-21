# Capstone Project Architecture

This document outlines the architecture of the Capstone project, detailing the structure and technologies used for both the backend and frontend.

## Backend Architecture

The backend is a Python-based RESTful API built with the **FastAPI** framework. It follows a layered architecture to ensure separation of concerns and maintainability.

- **Technology Stack:**
  - **Framework:** FastAPI
  - **Language:** Python 3.11+
  - **Database:** SQLite
  - **Data Validation:** Pydantic
  - **AI/LLM Integration:** Google Gemini, LangChain

- **Directory Structure (`backend/app`):**
  - `api/`: Contains the API endpoints (routers). `routes.py` defines all the paths and connects them to the service layer.
  - `core/`: Core application logic, including database configuration (`database.py`) and settings management (`config.py`).
  - `models/`: Pydantic models for data validation (API requests/responses) and SQLAlchemy models for database schema (`database_models.py`).
  - `services/`: The business logic layer. This is where interactions with databases, external APIs, and the LLM occur.
    - `recipe_service.py`: Handles all logic related to recipe generation, variations, and agent interactions.
    - `database_service.py`: Manages direct database operations.

## Frontend Architecture

The frontend is a modern web application built with **Next.js**, a React framework. It leverages TypeScript for type safety and TailwindCSS for styling.

- **Technology Stack:**
  - **Framework:** Next.js
  - **Language:** TypeScript
  - **UI Library:** React
  - **Styling:** TailwindCSS
  - **UI Components:** A combination of custom components and headless primitives from Radix UI, styled with TailwindCSS (e.g., located in `src/components/ui`).

- **Directory Structure (`frontend/src`):**
  - `app/`: The main application directory following the Next.js App Router convention. Each folder represents a route.
  - `components/`: Contains reusable React components.
    - `ui/`: Basic, reusable UI elements like `Button.tsx`, `Card.tsx`, `Dialog.tsx`.
  - `services/`: Handles communication with the backend API. `api.ts` centralizes all fetch requests into a single `ApiService` class.
  - `types/`: TypeScript type definitions and interfaces (e.g., `recipe.ts`).
  - `lib/`: Utility functions, like `cn` for merging TailwindCSS classes.

This structure allows for a scalable and maintainable codebase on both the frontend and backend.
