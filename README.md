# AI Agent Memory System

## Overview
A sophisticated memory system for AI agents, featuring reinforcement learning (RL) optimized retrieval, session management, and long-term memory storage. This system allows agents to store user interactions, retrieve relevant context, and learn from feedback to improve memory ranking over time.

## Key Features
- **RL-Optimized Retrieval:** Uses a Reinforcement Learning agent to rank and retrieve the most relevant memories.
- **Vector Search:** Powered by FAISS for efficient similarity search of context chunks.
- **Session Management:** Supports multiple chat sessions with persistent history.
- **Document Knowledge Base:** Upload and index PDF documents for knowledge retrieval.
- **Dual Memory Types:** Handles both conversational context and static knowledge (documents).
- **Feedback Loop:** Mechanisms to apply feedback to memory rankings, enabling the system to learn.

## Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **AI/ML:** FAISS, NumPy
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Utilities:** Lucide Icons

## Setup & Installation

### Prerequisites
- Python 3.8+

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Open `index.html` in your preferred web browser.
   - Alternatively, serve it using a simple HTTP server for a better experience:
     ```bash
     python -m http.server 8080
     ```
     Then visit `http://localhost:8080`.

## Usage
1. **Start Chatting:** Open the frontend and send a message. A new session ID will be generated automatically.
2. **Switch Sessions:** Use the sidebar to switch between past conversations.
3. **Upload Documents:** Click the upload button to add PDF documents to the knowledge base.
4. **Memory Retrieval:** The system automatically retrieves relevant context for each query based on vector similarity and RL ranking.

## Project Structure
```
ai-memory-system/
├── backend/            # FastAPI application
│   ├── app/            # Core application logic
│   │   ├── api/        # API Routes
│   │   ├── memory/     # Memory store & FAISS logic
│   │   ├── rl/         # Reinforcement Learning agent
│   │   ├── services/   # Business logic (MemoryService)
│   │   └── main.py     # Entry point
│   ├── data/           # Stored indices and data
│   └── requirements.txt
└── frontend/           # Web interface
    ├── index.html
    ├── script.js
    └── style.css
```

