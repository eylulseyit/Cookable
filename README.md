# AI-Powered Recipe Recommendation App

## 🍳 Recipe Recommendation App

An AI-powered recipe recommendation application that suggests recipes based on available ingredients, with advanced AI assistant features and shopping list generation.

## ✨ Key Features

- **AI-Powered Recipe Generation**: Get unique recipes based on ingredients you have.
- **Gourmet Assistant Agent**: Ask for recipe variations, drink pairings, and presentation tips.
- **Shopping List Generation**: Automatically generate a shopping list for missing ingredients.
- **Retrieval-Augmented Generation (RAG)**: Efficiently retrieve similar recipes from a vector database.

## 🚀 Tech Stack

- **Backend**: Python 3.12 + FastAPI
- **Frontend**: Next.js (React) + TypeScript + TailwindCSS
- **AI**: Google Gemini LLM + LangChain
- **Database**: SQLite
- **Vector Database**: ChromaDB
- **Deployment**: Vercel (Frontend) + Railway (Backend) (Planned for Phase 5)

## 📁 Project Structure

```
CapstoneProject/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/                 # API endpoints (routers)
│   │   ├── core/                # Core configurations (database, settings)
│   │   ├── models/              # Pydantic and SQLAlchemy models
│   │   └── services/            # Business logic and AI integrations
│   ├── requirements.txt
│   ├── main.py                  # Main FastAPI application entry
│   └── init_db.py               # Database initialization script
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/                 # Next.js App Router routes
│   │   ├── components/          # Reusable React components
│   │   │   └── ui/              # Shadcn/UI (Radix UI + TailwindCSS) components
│   │   ├── services/            # API service calls
│   │   └── types/               # TypeScript type definitions
│   ├── package.json
│   └── next.config.ts
├── ARCHITECTURE.md          # Detailed project architecture documentation
├── TASKS.md                 # Project development tasks
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

1.  **Open a new terminal.**
2.  **Navigate to the project root directory:**
    ```bash
    cd C:\Users\ey-lu\Desktop\computer-engineering\vscode\CapstoneProject
    ```
3.  **Create and activate the virtual environment (if not already done):**
    ```bash
    cd backend
    python -m venv venv
    . .\venv\Scripts\activate  # On Windows PowerShell
    # On Git Bash/WSL: source venv/bin/activate
    cd .. # Return to project root
    ```
4.  **Install backend dependencies:**
    ```bash
    C:\Users\ey-lu\Desktop\computer-engineering\vscode\CapstoneProject\backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
    ```
5.  **Initialize the database (run once):**
    ```bash
    C:\Users\ey-lu\Desktop\computer-engineering\vscode\CapstoneProject\backend\venv\Scripts\python.exe backend/init_db.py
    ```
6.  **Start the backend server:**
    ```bash
    C:\Users\ey-lu\Desktop\computer-engineering\vscode\CapstoneProject\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload
    ```
    The backend should now be running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Open another new terminal.**
2.  **Navigate to the frontend directory:**
    ```bash
    cd C:\Users\ey-lu\Desktop\computer-engineering\vscode\CapstoneProject\frontend
    ```
3.  **Install frontend dependencies:**
    ```bash
    npm install
    ```
4.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend should now be running at `http://localhost:3000`.

## 🎯 User Flow

1.  **Ingredient Input**: User enters available ingredients into a dedicated input field.
2.  **AI Recipe Generation**: The backend processes the ingredients using Google Gemini LLM and generates a unique recipe.
3.  **Recipe Display**: The suggested recipe is displayed with details like title, ingredients, instructions, cooking time, and difficulty.
4.  **Shopping List**: A generated shopping list highlights ingredients the user needs to purchase.
5.  **Gourmet Assistant**: Users can interact with an AI agent to get:
    *   Recipe variations
    *   Drink pairings
    *   Presentation tips
6.  **Recipe Refinement**: Users can refine the current recipe based on agent suggestions.
7.  **Explore More**: Users can start a new query or explore other options.

## 🔧 Development Phases

-   **Phase 1: Idea and Planning (Completed)**
    *   Problem definition and idea generation (documented in PRD.md).
    *   User flow and technology selection (defined in PRD.md).

-   **Phase 2: Coding and AI Integration (Completed)**
    *   GitHub repository setup and project structuring.
    *   Core feature development (Ingredient Input -> AI Recipe Output).
    *   Google Gemini LLM integration.

-   **Phase 3: Automation and Agent Logic (Half-Working)**
    *   Recipe analysis and shopping list generation implemented.
    *   Advanced "Gourmet Assistant Agent" using LangChain, including: Recipe Variation Tool, Drink Pairing Tool, and Presentation Tip Tool.
    *   Agent API endpoint and frontend integration (buttons, modern UI for results).

-   **Phase 4: RAG or Fine-tuning Implementation (Broken)**
    *   VectorDB integration (ChromaDB) to store existing recipes.
    *   Retrieval-Augmented Generation (RAG) system to find best matching recipes based on user ingredients from VectorDB.

-   **Phase 5: Deployment and Demo (Pending)**
    *   Frontend deployment to Vercel.
    *   Backend deployment to Railway.
    *   Project landing page creation.
    *   Project demo video or GIF preparation.

## 📝 License

MIT License 
