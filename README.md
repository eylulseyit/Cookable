# AI-First Development Capstone Project

## 🍳 Recipe Recommendation App

An AI-powered recipe recommendation application that suggests recipes based on available ingredients.

## 🚀 Tech Stack

- **Backend**: Python 3.12 + FastAPI
- **Frontend**: Next.js (React)
- **AI**: Open Source LLMs
- **Database**: PostgreSQL
- **Deployment**: Vercel (Frontend) + Railway (Backend)

## 📁 Project Structure

```
CapstoneProject/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── requirements.txt
│   └── main.py
├── frontend/                # Next.js frontend
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── package.json
├── docs/                    # Documentation
└── README.md
```

## 🛠️ Setup Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🎯 User Flow

1. **Home Page** - User sees a simple interface to enter ingredients
2. **Ingredient Input** - User types available ingredients
3. **Optional Filters** - User can select dietary preferences
4. **AI Recipe Suggestion** - Backend processes ingredients with AI
5. **Recipe Display** - User views suggested recipe with details
6. **New Query/Exit** - User can start over or exit

## 🔧 Development Phases

- **Phase 1**: Basic backend API with FastAPI
- **Phase 2**: Frontend with Next.js
- **Phase 3**: AI integration
- **Phase 4**: Database integration
- **Phase 5**: Deployment

## 📝 License

MIT License 