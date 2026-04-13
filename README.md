# AskQuery

A lightweight **Retrieval-Augmented Generation (RAG)** based AI assistant that enables students to query university databases in natural language. AskQuery combines semantic search with generative AI to provide accurate, context-aware answers about departments, faculty, events, courses, and academic calendars.

## 🎯 Overview

AskQuery bridges the gap between unstructured student questions and structured university data. Instead of remembering specific database queries or navigating complex systems, students can simply ask their questions in English, and the system retrieves relevant information and generates natural language responses.

**Key Use Cases:**
- "Which departments does the university have?"
- "Who are the assistant professors in the Economics department?"
- "When is the academic calendar for 2024?"
- "What events are happening next month?"
- "What are the prerequisites for DSA?"

## ✨ Features

- **🗣️ Natural Language Interface**: Ask questions in plain English without knowing SQL or database structure
- **🧠 RAG Pipeline**: Combines retrieval (FAISS vector store + Postgres) with generation (Google Gemini) for accurate, grounded responses
- **⚡ CPU-Optimized**: Uses E5-small-v2 embeddings for efficient retrieval without requiring GPUs
- **🔒 Secure Authentication**: Integrates Supabase for user authentication and session management
- **🎨 Modern Web UI**: Clean, responsive Next.js interface with light/dark theme support
- **📊 Multi-Source Data**: Queries multiple database tables (departments, faculty, events, courses, academic calendar)
- **📝 Query Logging**: Tracks retrieval performance and user queries for debugging and optimization

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python) with async support
- **LLM**: Google Generative AI (Gemini 3 Flash Preview)
- **Vector Store**: PostgreSQL with pgvector extension (via LlamaIndex)
- **Embeddings**: Hugging Face E5-small-v2 (384-dim, CPU-friendly)
- **Retrieval**: LlamaIndex with custom vector store indexing
- **Authentication**: Supabase JWT with bearer tokens
- **Logging**: Python logging module (system.log, retrieval_debug.log)

### Frontend
- **Framework**: Next.js 14+ with React
- **Language**: TypeScript + JSX
- **UI Components**: Radix UI (accordion, dialog, dropdown, etc.)
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Authentication**: Supabase Auth

### Database
- **Primary Database**: PostgreSQL (Supabase) with vector extension
- **Tables**:
  - `departments` - University departments
  - `faculty` - Faculty members with designations
  - `subjects` - Course subjects
  - `playlists` - Learning resource links (YouTube playlists)
  - `events` - University events
  - `academic_calendar` - Academic calendar events
  - `documents` - Vector embeddings (auto-populated)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│  - AIAssistantUI, ChatPane, Sidebar, AuthModal             │
│  - Authentication: Supabase JWT                            │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Backend (FastAPI)                           │
│  - /health → Health check                                   │
│  - /ask → Query (requires Supabase token)                   │
│  - CORS enabled for frontend access                         │
└────────────┬──────────────────────────────────┬─────────────┘
             │                                  │
             ▼                                  ▼
    ┌────────────────────┐          ┌─────────────────────┐
    │  Answer Generation │          │  Retrieval Engine   │
    │  (GeminiEngine)    │          │  (LlamaIndex)       │
    │  - Gemini 3 Flash  │          │  - E5-small-v2 EMB  │
    │  - Prompt + Context│          │  - pgvector Store   │
    └────────────────────┘          │  - Similarity Top-K │
             ▲                       └──────────┬──────────┘
             │                                  │
             └──────────────────┬───────────────┘
                                │
                        ┌───────▼─────────┐
                        │   PostgreSQL    │
                        │   (Supabase)    │
                        │ - departments   │
                        │ - faculty       │
                        │ - subjects      │
                        │ - playlists     │
                        │ - events        │
                        │ - calendar      │
                        │ - documents (πi)│
                        └─────────────────┘
```

### Query Flow:
1. **User Input**: Student asks a question via Next.js frontend
2. **Authentication**: Supabase JWT token validated by FastAPI
3. **Retrieval**: Question embeddings created (E5-small-v2), matched against vector store (pgvector)
4. **Filtering**: Top-K results (similarity_top_k=5, cutoff=0.3) extracted
5. **Generation**: Retrieved context + question sent to Gemini 3 Flash
6. **Response**: Natural language answer returned to frontend
7. **Logging**: Query, retrieved chunks, and response logged for debugging

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- PostgreSQL 14+ with pgvector extension (use Supabase for managed solution)
- pnpm or npm (package manager)
- API Access:
  - Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikeys))
  - Supabase project ([Create one here](https://supabase.com))

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/srivastavaprakhar/AskQuery.git
   cd AskQuery
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Create `.env` file in the project root**
   ```bash
   cat > .env << 'EOF'
   # Google Gemini API
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Supabase Configuration
   DATABASE_URL=postgresql://postgres.xxxxx:password@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?sslmode=require
   SUPABASE_DB_PASSWORD=your_db_password
   SUPABASE_DB_HOST=your-project.pooler.supabase.com
   SUPABASE_DB_NAME=postgres
   SUPABASE_DB_USER=postgres.xxxxx
   SUPABASE_DB_PORT=6543
   SUPABASE_URL=https://your-project.supabase.co
   
   # Optional: Local model path (not needed for Gemini API)
   MODEL_PATH=
   EOF
   ```

### Backend Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL Database**
   
   Option A: Use Supabase (Recommended)
   - Create a new Supabase project
   - Enable pgvector extension: `CREATE EXTENSION IF NOT EXISTS vector;`
   - Update DATABASE_URL in `.env` with your Supabase connection string

   
   Option B: Local PostgreSQL
   - Install PostgreSQL locally and create a database
   - Install pgvector: `CREATE EXTENSION vector;`
   - Update DATABASE_URL in `.env`

3. **Initialize database tables** (run once)
   ```bash
   python database/cse.py
   python database/department_faculty.py
   python database/subjects_playlist.py
   python database/events_academic_events.py
   ```
   This creates and populates:
   - `departments` table
   - `faculty` table
   - `subjects` table
   - `playlists` table
   - `events` table
   - `academic_calendar` table

4. **Start the backend server**
   ```bash
   python api_wrapper.py
   ```
   Expected output:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete
   ```
   
   On first run:
   - Backend initializes GeminiEngine (loads Gemini API config)
   - Builds FAISS index from Postgres data (may take 1-2 minutes)
   - Creates pgvector embeddings for all documents
   - Sets up logging to `logs/system.log` and `logs/retrieval_debug.log`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Create `.env.local` file** (optional - defaults are already set)
   ```bash
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   ```

3. **Install frontend dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   pnpm dev
   ```
   Frontend starts at `http://localhost:3000`

5. **Production build** (optional)
   ```bash
   npm run build
   npm run start
   ```

## 📖 Using the Application

### Web Interface
1. Open browser to `http://localhost:3000`
2. Sign up or login with Supabase credentials
3. Type your question in the chat input
4. The AI will:
   - Search the vector store for relevant documents
   - Retrieve context from Postgres tables
   - Generate a natural language response
   - Display the answer in the chat

### Example Questions
```
"Which all departments does the university consist of?"
→ Returns list of all departments from the departments table

"Who are all assistant professors in Economics?"
→ Retrieves faculty with specific designation from faculty table

"List all events happening in 2024"
→ Searches events table for 2024 entries

"What topics are covered in DSA?"
→ Retrieves learning resources and course details

"When is the academic registration?"
→ Fetches dates from academic_calendar table
```

### CLI Interface (Testing)
Optionally test via command line before using the web interface:
```bash
python main.py
# Select login or signup
# Type your question and get responses
```

## 📡 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### Health Check
```http
GET /health
```
**Purpose**: Verify backend is running
**Response**:
```json
{
  "status": "ok"
}
```

#### Ask Question
```http
POST /ask
Authorization: Bearer <supabase_jwt_token>
```

**Request Body**:
```json
{
  "question": "Which departments are available?"
}
```

**Response**:
```json
{
  "answer": "The university consists of the following departments: Department of Computer Science and Engineering, Department of Economics, Department of Journalism and Mass Communication, and Department of Languages, Literatures and Cultural Studies."
}
```

**Error Responses**:
```json
{
  "detail": "Invalid or expired token"  // 401 Unauthorized
}
```

```json
{
  "detail": "Error generating response"  // 500 Server Error
}
```

**Note**: Requires valid Supabase JWT token. The frontend automatically handles token verification.

## 📋 Database Schema

### departments
```sql
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name TEXT UNIQUE NOT NULL
);
```
**Departments**:
- Department of Economics
- Department of Journalism and Mass Communication
- Department of Languages, Literatures and Cultural Studies
- Department of Arts
- Department of Computer Science & Engineering

### faculty
```sql
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(department_id) ON DELETE CASCADE
);
```
**Designations included**:
- Professor
- Associate Professor
- Assistant Professor (various scales)
- Senior Faculty Members

### subjects
```sql
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name TEXT UNIQUE NOT NULL
);
```
**Available Subjects**:
- DAA (Design and Analysis of Algorithms)
- DSA (Data Structures and Algorithms)
- Operating System
- Automata and Compiler Design
- Java OOPs

### playlists
```sql
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
    url TEXT NOT NULL
);
```
Contains YouTube playlist links for each subject (2+ playlists per subject)

### events
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    event_date TEXT,
    location TEXT
);
```
**Sample Events**:
- #include (Tech competition) - Feb 22, 2025
- ACM ROCS - Nov 23, 2024
- International Symposium for Data Science - Nov 7-8, 2024
- Elicit'24 (Techno Cultural Fest) - Sep 27-29, 2024
- Job Junction - Apr 15-16, 2024

### academic_calendar
```sql
CREATE TABLE academic_calendar (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    description TEXT
);
```
**Sample Events**:
- Opening of fee payment portal - June 26, 2023
- PhD Entrance Examination - July 7, 2023
- Commencement of classes - July 11, 2023
- Tech fest/TEDx - Oct 14-15, 2023
- Mid Terms - Mar 4-8, 2024
- End Terms - May 3-17, 2024

### documents (Auto-populated)
```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP
);
```
Auto-generated from all other tables via postgres_loader.py

### Troubleshooting

#### "Failed to fetch" or "Cannot connect to backend server" Error

If you see this error in the frontend:

1. **Check if the backend is running:**
   - Make sure you've started the backend server with `python api_wrapper.py`
   - The backend should be running on `http://127.0.0.1:8000`
   - You should see startup messages in the terminal where you ran the backend

2. **Verify the backend is accessible:**
   - Open your browser and navigate to `http://127.0.0.1:8000/health`
   - You should see `{"status":"ok"}` if the backend is running

3. **Check the backend logs:**
   - Look at the terminal where you started the backend
   - Check `logs/system.log` for any errors

4. **Verify the API URL:**
   - The frontend defaults to `http://127.0.0.1:8000`
   - If your backend runs on a different port, create a `.env.local` file in the `frontend` directory:
     ```
     NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
     ```

5. **Backend startup time:**
   - The backend may take a while to start (loading the model)
   - Wait for the model to load before trying to connect
   - The frontend will automatically retry the connection

#### Backend Model Loading Issues

- If using a local GGUF model: ensure the model file exists at the path specified in `config.py` or the `MODEL_PATH` env var.
- If using Google Gemini (cloud): ensure `GEMINI_API_KEY` is set and your network allows outbound API calls.
- For local models, check that you have enough disk space and memory — model files can be several GB.

## Usage

- Query the database with questions like:
  > "Which all departments does the university consist of?"

- Responses are generated using the RAG pipeline for accuracy and context.

## Model Details

- **Embeddings**: [MiniLM/E5](https://huggingface.co/MiniLM)
- **LLM**: Google Gemini (via `GeminiEngine`)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
- **Relational DB**: [SQLite](https://www.sqlite.org/index.html)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

- [Google Gemini Docs](https://developers.generativeai.google/)
- [Facebook FAISS](https://github.com/facebookresearch/faiss)
- [Hugging Face](https://huggingface.co/)
