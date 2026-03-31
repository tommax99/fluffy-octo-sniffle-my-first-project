# CollabTask Manager - Real-time Collaborative Task Management Platform

A full-stack, real-time collaborative task management application built with modern technologies.

## 🚀 Features

### Backend (FastAPI + SQLAlchemy + Redis)
- **RESTful API** with OpenAPI/Swagger documentation
- **Real-time WebSocket** support for live updates
- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (Admin, Project Manager, Member)
- **Event-driven architecture** using Redis Pub/Sub
- **Async database operations** with SQLAlchemy 2.0
- **Pydantic V2** for data validation
- **Comprehensive test suite** with pytest

### Frontend (React + TypeScript + Vite)
- **Real-time collaboration** with WebSocket integration
- **Drag-and-drop Kanban board** with dnd-kit
- **Redux Toolkit** for state management
- **React Query** for server state management
- **TailwindCSS** for styling
- **Type-safe** with TypeScript
- **Responsive design** for all devices

### Core Entities
- **Users** with authentication and profiles
- **Workspaces** for team organization
- **Projects** with customizable workflows
- **Tasks** with subtasks, attachments, and comments
- **Labels** and **Tags** for organization
- **Activity Logs** for audit trails

## 📁 Project Structure

```
collab-task-manager/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration, security, dependencies
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access layer
│   │   └── events/       # Event handlers and pub/sub
│   └── tests/            # Test suite
├── frontend/
│   └── src/
│       ├── components/   # React components
│       ├── hooks/        # Custom React hooks
│       ├── services/     # API clients
│       ├── store/        # Redux store
│       ├── types/        # TypeScript types
│       └── utils/        # Utility functions
└── docs/                 # Documentation
```

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (Async)
- PostgreSQL
- Redis
- Pydantic V2
- Passlib (password hashing)
- PyJWT
- WebSockets

### Frontend
- React 18
- TypeScript
- Vite
- Redux Toolkit
- React Query
- TailwindCSS
- dnd-kit (drag and drop)
- Socket.io-client

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📄 License

MIT License

## 👥 Contributing

Contributions are welcome! Please read our contributing guidelines first.
