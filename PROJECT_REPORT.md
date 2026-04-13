# AskQuery — Project Report

---

## 1. Introduction

In today's digital era, universities generate large volumes of structured data — faculty records, department listings, course information, academic calendars, events, and more. Students and staff often find it difficult to navigate these databases or remember precise terminology to locate information. Traditional query interfaces require knowledge of database schemas or SQL, making them inaccessible to the average user.

**AskQuery** is a Retrieval-Augmented Generation (RAG) based AI assistant built specifically for Manipal University Jaipur. It allows students and university users to ask questions in plain, natural English — such as "Who are the assistant professors in the Economics department?" or "When do mid-term exams begin?" — and receive accurate, conversational answers pulled directly from the university's structured database.

The system bridges the gap between unstructured human language and structured relational data by combining:
- **Semantic vector search** (using pgvector and E5-small-v2 embeddings) to find relevant database records, and
- **Google Gemini 3 Flash**, a large language model, to generate natural, fluent answers from the retrieved context.

AskQuery provides a clean, modern web interface built in Next.js with Supabase-powered authentication, ensuring only authorized users can query the system.

---

## 2. Objective of the Project

*(As proposed in synopsis)*

The primary objectives of the AskQuery project are:

1. **To develop a natural language interface** for querying structured university databases, eliminating the need for SQL knowledge or complex navigation.
2. **To implement a Retrieval-Augmented Generation (RAG) pipeline** that combines semantic search with a large language model for accurate, context-grounded responses.
3. **To build a secure, authenticated web application** using modern full-stack technologies (Next.js frontend + FastAPI backend + Supabase Auth).
4. **To integrate a vector database** (PostgreSQL with pgvector extension) for efficient similarity-based retrieval from university data.
5. **To make the system CPU-friendly** by using lightweight embeddings (E5-small-v2, 384 dimensions) that do not require GPU hardware.
6. **To log and monitor system activity** including user queries and retrieval quality for future optimization.

---

## 3. Brief Description of the Project

AskQuery is a full-stack web application that enables university users to query institutional data using natural language. The application is composed of three major layers:

**Frontend (Next.js + React + TypeScript):**
A responsive, modern chat interface styled with Tailwind CSS. Users log in via Supabase authentication (email/password), then interact with the AI through a chat panel. The interface supports multiple conversation threads, pinned chats, dark/light themes, and a sidebar for navigation.

**Backend (FastAPI + Python):**
A RESTful API server exposes two endpoints — `/health` for system status, and `/ask` for authenticated query processing. On startup, the backend initializes the Gemini LLM engine and builds a vector index from PostgreSQL data. Each incoming question is embedded using E5-small-v2, matched against the pgvector index, and the top retrieved chunks are sent as context to the Gemini model, which generates a natural language response.

**Database (PostgreSQL via Supabase):**
The university's structured data is stored across six relational tables (departments, faculty, subjects, playlists, events, academic_calendar). A seventh table, `documents`, stores vector embeddings automatically generated from all other tables. Supabase also manages user authentication.

The system also includes a CLI interface (`main.py`) for direct terminal-based testing and a collection of database population scripts under the `database/` folder.

---

## 4. Technology Used

### Programming Languages
| Language   | Usage                                          |
|------------|------------------------------------------------|
| Python 3.8+| Backend API, RAG pipeline, database scripts    |
| TypeScript | Frontend (Next.js components, type-safe code)  |
| JavaScript | Frontend React components (JSX)                |
| SQL        | PostgreSQL table creation and data queries     |
| Bash       | Server startup script (`start.sh`)             |

### Frameworks & Libraries — Backend
| Technology              | Version / Notes                                                        |
|-------------------------|------------------------------------------------------------------------|
| FastAPI                 | Python web framework for the REST API                                  |
| Uvicorn                 | ASGI server for running FastAPI                                        |
| LlamaIndex (Core)       | RAG orchestration — VectorStoreIndex, query engine, node parsers       |
| LlamaIndex pgvector     | PostgreSQL vector store integration for LlamaIndex                     |
| google-generativeai     | Google Gemini 3 Flash Preview LLM for answer generation                |
| Hugging Face Transformers | E5-small-v2 sentence embedding model (384-dim, CPU-optimized)        |
| PyTorch                 | Model inference for embedding generation                               |
| psycopg2-binary         | PostgreSQL database driver                                             |
| python-jose             | JWT token handling for Supabase authentication                         |
| python-dotenv           | Environment variable management                                        |
| bcrypt                  | Password hashing (CLI auth)                                            |
| requests                | HTTP client for Supabase Auth API calls                                |

### Frameworks & Libraries — Frontend
| Technology              | Version / Notes                                                        |
|-------------------------|------------------------------------------------------------------------|
| Next.js                 | 16.x — React-based full-stack web framework                            |
| React                   | 18.x — UI component library                                            |
| Tailwind CSS            | 4.x — Utility-first CSS framework                                      |
| Radix UI                | Accessible headless UI components (dialog, dropdown, tabs, etc.)       |
| @supabase/supabase-js   | 2.x — Supabase client for auth and database                            |
| Lucide React            | Icon library                                                           |
| Framer Motion           | Animation library                                                      |
| @vercel/analytics       | Web analytics                                                          |

### Infrastructure & Services
| Technology       | Role                                                                  |
|------------------|-----------------------------------------------------------------------|
| Supabase         | Managed PostgreSQL database + pgvector extension + user authentication|
| PostgreSQL 14+   | Primary relational database with vector search capability             |
| pgvector         | PostgreSQL extension enabling vector similarity search                 |
| Google Gemini    | Cloud LLM API for natural language answer generation                  |
| Vercel           | Frontend deployment platform (Next.js hosting)                        |

---

## 5. Hardware Requirements

| Component      | Minimum Requirement                                    |
|----------------|--------------------------------------------------------|
| Processor      | Intel Core i3 / AMD equivalent, 1.5 GHz or higher     |
| RAM            | 4 GB (8 GB recommended for running embedding model)    |
| Storage        | 2 GB free disk space for dependencies and model files  |
| Network        | Stable broadband internet connection (for API calls)   |
| Display        | 1280×720 resolution or higher                          |
| GPU            | Not required — system is CPU-optimized                 |

**Server/Deployment Requirements:**
- Backend server: 1 vCPU, 2 GB RAM minimum (Supabase handles the database)
- Frontend hosting: Vercel free tier is sufficient

---

## 6. Software Requirements

### Development Environment
| Software           | Version       | Purpose                                       |
|--------------------|---------------|-----------------------------------------------|
| Operating System   | Windows 10+, Ubuntu 20.04+, or macOS 12+ | Development platform      |
| Python             | 3.8 or higher | Backend runtime                               |
| Node.js            | 18 or higher  | Frontend runtime and build tool               |
| pnpm / npm         | Latest        | Node.js package manager                       |
| Git                | Latest        | Version control                               |

### Runtime Dependencies
| Software           | Purpose                                               |
|--------------------|-------------------------------------------------------|
| PostgreSQL 14+     | Database server (or Supabase cloud instance)          |
| pgvector extension | Vector similarity search in PostgreSQL                |
| Web Browser        | Chrome, Firefox, or Edge (for frontend access)        |

### API Keys / Accounts Required
| Service       | Purpose                                                      |
|---------------|--------------------------------------------------------------|
| Google Gemini | API key from Google AI Studio for LLM answer generation      |
| Supabase      | Project URL, anon key, and database credentials              |

### Environment Variables (`.env`)
```
GEMINI_API_KEY=<Google Gemini API key>
DATABASE_URL=<Supabase PostgreSQL connection string>
SUPABASE_DB_HOST=<Supabase DB host>
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=<Supabase DB user>
SUPABASE_DB_PASSWORD=<Supabase DB password>
SUPABASE_DB_PORT=6543
SUPABASE_URL=<Supabase project URL>
SUPABASE_ANON_KEY=<Supabase anonymous key>
```

---

## 7. Organization Profile

**Manipal University Jaipur (MUJ)**

AskQuery is developed in the context of Manipal University Jaipur, a leading private university located in Jaipur, Rajasthan, India. The university is a constituent unit of the Manipal Education and Medical Group (MEMG) and is recognized by the University Grants Commission (UGC).

The university offers undergraduate, postgraduate, and doctoral programs across a wide range of disciplines, including Computer Science and Engineering, Economics, Journalism and Mass Communication, Languages, Literatures and Cultural Studies, and Fine Arts.

The university's data — including its departments, faculty members, academic calendar, course subjects, and campus events — forms the core knowledge base that AskQuery queries against. Example departments in the system include:
- Department of Computer Science & Engineering
- Department of Economics
- Department of Journalism and Mass Communication
- Department of Languages, Literatures and Cultural Studies
- Department of Arts

*(AskQuery is an individual/academic software project developed to demonstrate the practical application of RAG-based AI systems on institutional data.)*

---

## 8. Design Description

AskQuery follows a **three-tier architecture** with a clean separation of concerns:

### Tier 1 — Presentation Layer (Frontend)
The Next.js frontend is the interface through which users interact with the system. Key UI components include:
- **AIAssistantUI**: Top-level component managing state for conversations, authentication, and theme.
- **AuthModal**: Email/password login and signup form backed by Supabase Auth.
- **Sidebar**: Lists all conversation threads with search, pin, and collapse functionality.
- **ChatPane**: Displays message history and a message composer. Supports edit and resend of messages.
- **Message**: Renders individual chat bubbles with distinct styles for user and AI messages.
- **Header**: Top bar with navigation controls.
- **ThemeToggle**: Switches between light and dark themes.

Conversations are persisted to `localStorage` so users retain their chat history across browser sessions.

### Tier 2 — Application/Business Logic Layer (Backend)
The FastAPI backend (`api_wrapper.py`) orchestrates all processing:
- **Authentication Middleware**: Every `/ask` request must carry a valid Supabase JWT bearer token. The token is verified against the Supabase Auth API.
- **Startup Initialization** (`@app.on_event("startup")`): On server start, a background thread initializes the Gemini LLM engine and builds the LlamaIndex vector store from PostgreSQL data.
- **Query Processing** (`answer_question` in `main.py`):
  1. The user's question is embedded using E5-small-v2.
  2. The vector index is queried (`similarity_top_k=5`, `similarity_cutoff=0.3`).
  3. Retrieved context chunks are filtered (score ≥ 0.5; fallback to top 3 if none qualify).
  4. A structured prompt is sent to Gemini 3 Flash: includes the student's question and the factual context.
  5. The generated answer is returned to the frontend.
- **Logging**: System events and retrieval debug info are written to `logs/system.log` and `logs/retrieval_debug.log`.

### Tier 3 — Data Layer (PostgreSQL + pgvector)
The Supabase-hosted PostgreSQL database stores:
- **Structured relational data**: Six domain tables (departments, faculty, subjects, playlists, events, academic_calendar).
- **Vector embeddings**: The `documents` table stores 384-dimensional E5-small-v2 embeddings for all records, enabling semantic similarity search.

The `postgres_loader.py` module fetches all rows from all public tables, resolves foreign key relationships, and creates LlamaIndex `Document` objects. The `embed_and_index.py` module creates embeddings and builds the `PGVectorStore` index.

---

## 9. Flow Chart

```
┌────────────────────────────────────────────────────────┐
│                        START                           │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ User opens AskQuery  │
              │ web application      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Is user logged in?   │
              └──────────┬───────────┘
                    No   │   Yes
          ┌──────────────┘   └────────────────┐
          ▼                                   ▼
┌──────────────────────┐         ┌────────────────────────┐
│ Show Auth Modal      │         │ Show Chat Interface    │
│ (Login / Sign Up)    │         │ (Sidebar + ChatPane)   │
└──────────┬───────────┘         └────────────┬───────────┘
           │                                  │
           ▼                                  ▼
┌──────────────────────┐         ┌────────────────────────┐
│ Validate credentials │         │ User types a question  │
│ via Supabase Auth    │         └────────────┬───────────┘
└──────────┬───────────┘                      │
     Auth  │  Fail                            ▼
    Success│  ─► Show error               ┌────────────────────────┐
           │                              │ Frontend sends POST     │
           ▼                              │ /ask with JWT token     │
┌──────────────────────┐                 └────────────┬───────────┘
│ Store session token  │                              │
│ Redirect to Chat UI  │                              ▼
└──────────────────────┘              ┌────────────────────────┐
                                      │ Backend verifies JWT   │
                                      │ via Supabase Auth API  │
                                      └────────────┬───────────┘
                                           Valid   │  Invalid
                                                   │  ─► 401 Unauthorized
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Embed question with    │
                                      │ E5-small-v2 model      │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Query pgvector store   │
                                      │ (Top-K similarity      │
                                      │  search, K=5)          │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Filter chunks          │
                                      │ (score ≥ 0.5)          │
                                      │ Fallback: top 3        │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Build prompt with      │
                                      │ context + question     │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Send to Gemini 3 Flash │
                                      │ Generate answer        │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Return JSON response   │
                                      │ {"answer": "..."}      │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Display answer in chat │
                                      │ Log query & response   │
                                      └────────────┬───────────┘
                                                   │
                                                   ▼
                                              ┌─────────┐
                                              │   END   │
                                              └─────────┘
```

---

## 10. Data Flow Diagrams (DFDs)

### Level 0 DFD — Context Diagram

```
                   ┌─────────────────────────────┐
                   │                             │
   Question ──────►│        AskQuery System      │──────► Answer
                   │                             │
   User ──────────►│  (Natural Language Query    │◄────── User
                   │   Processing & Response     │
                   │         System)             │
                   │                             │
                   └─────────────────────────────┘
                              ▲         │
                              │         │
                     Auth Credentials  Session Token
```

**External Entities:** University Student / Staff (User)
**System:** AskQuery (RAG-based query system)
**Input:** Natural language question + user credentials
**Output:** Natural language answer

---

### Level 1 DFD

```
┌─────────┐
│  USER   │
└────┬────┘
     │ Credentials          ┌──────────────────┐
     └─────────────────────►│   1. User Auth   │
                            │  (Supabase Auth) │
                            └────────┬─────────┘
     │ Question                      │ JWT Token
     └─────────────────────────────► ▼
                            ┌──────────────────┐
                            │ 2. Token         │
                            │  Verification    │
                            │  (FastAPI)       │
                            └────────┬─────────┘
                                     │ Verified Question
                                     ▼
                            ┌──────────────────┐
                            │ 3. Embedding     │
                            │  Generation      │
                            │ (E5-small-v2)    │
                            └────────┬─────────┘
                                     │ Question Vector
                                     ▼
                            ┌──────────────────┐        ┌─────────────────────┐
                            │ 4. Vector        │◄───────│   Documents Table   │
                            │  Similarity      │        │ (PostgreSQL/pgvector)│
                            │  Search          │        └─────────────────────┘
                            └────────┬─────────┘
                                     │ Top-K Context Chunks
                                     ▼
                            ┌──────────────────┐        ┌─────────────────────┐
                            │ 5. Prompt        │        │  All Domain Tables  │
                            │  Construction    │◄───────│ (departments,       │
                            │  & LLM Call      │        │  faculty, subjects, │
                            │ (Gemini Flash)   │        │  events, etc.)      │
                            └────────┬─────────┘        └─────────────────────┘
                                     │ Generated Answer
                                     ▼
                            ┌──────────────────┐
                            │ 6. Response      │
                            │  Logging &       │
                            │  Delivery        │
                            └────────┬─────────┘
                                     │ Answer JSON
                                     ▼
┌─────────┐
│  USER   │◄────────────── Natural Language Answer
└─────────┘
```

**Process Descriptions:**
1. **User Auth**: Supabase handles registration and login, issuing a JWT token upon success.
2. **Token Verification**: FastAPI's `/ask` endpoint verifies the bearer token against Supabase Auth API.
3. **Embedding Generation**: The user's question is converted to a 384-dimensional vector using E5-small-v2.
4. **Vector Similarity Search**: The question vector is matched against stored document embeddings in pgvector (Top-5 results, cutoff 0.3).
5. **Prompt Construction & LLM Call**: Retrieved context is injected into a structured prompt, then sent to Google Gemini 3 Flash for answer generation.
6. **Response Logging & Delivery**: The generated answer is logged and returned as JSON to the frontend.

---

## 11. Entity Relationship Diagram (E-R Diagram)

### Entities, Attributes, and Relationships

```
┌─────────────────────────┐           ┌─────────────────────────────┐
│        DEPARTMENTS       │           │           FACULTY            │
├─────────────────────────┤           ├─────────────────────────────┤
│ PK department_id SERIAL  │◄──────────│ PK faculty_id SERIAL         │
│    department_name TEXT  │  belongs  │    name TEXT                 │
│                          │    to     │    designation TEXT          │
└─────────────────────────┘           │ FK department_id INTEGER     │
                                       └─────────────────────────────┘

┌─────────────────────────┐           ┌─────────────────────────────┐
│         SUBJECTS         │           │          PLAYLISTS           │
├─────────────────────────┤           ├─────────────────────────────┤
│ PK subject_id SERIAL     │◄──────────│ PK playlist_id SERIAL        │
│    subject_name TEXT     │  has      │ FK subject_id INTEGER        │
│                          │           │    url TEXT                  │
└─────────────────────────┘           └─────────────────────────────┘

┌─────────────────────────┐
│          EVENTS          │
├─────────────────────────┤
│ PK id INTEGER            │
│    title TEXT            │
│    description TEXT      │
│    event_date TEXT       │
│    location TEXT         │
└─────────────────────────┘

┌─────────────────────────┐
│     ACADEMIC_CALENDAR    │
├─────────────────────────┤
│ PK id INTEGER            │
│    title TEXT            │
│    start_date TEXT       │
│    end_date TEXT         │
│    description TEXT      │
└─────────────────────────┘

┌─────────────────────────────────────────┐
│               DOCUMENTS                  │
│           (Auto-populated)               │
├─────────────────────────────────────────┤
│ PK id BIGSERIAL                          │
│    content TEXT                          │
│    embedding vector(384)                 │
│    metadata JSONB                        │
│    created_at TIMESTAMP                  │
└─────────────────────────────────────────┘
   (derived from all other tables via
    postgres_loader.py at index build time)
```

### Relationships Summary
| Relationship         | Type          | Description                                              |
|----------------------|---------------|----------------------------------------------------------|
| faculty → departments| Many-to-One   | Each faculty member belongs to one department            |
| playlists → subjects | Many-to-One   | Each playlist is linked to one subject                   |
| documents ← all tables | Derived     | Documents table is auto-populated from all domain tables |

---

## 12. Project Description

### Overview
AskQuery is an AI-powered university information assistant that allows students and staff to query the university's structured database using plain English. Instead of navigating forms or knowing SQL, users can simply type questions into a chat interface and receive instant, accurate answers.

### System Architecture
The system is built on the RAG (Retrieval-Augmented Generation) paradigm:
1. **Retrieval**: When a question is asked, it is embedded into a 384-dimensional vector using the E5-small-v2 model. This vector is compared against pre-computed embeddings of all university database records stored in PostgreSQL's pgvector extension. The most semantically similar records (Top-5) are retrieved.
2. **Augmentation**: The retrieved records are formatted as context and injected into a prompt template.
3. **Generation**: Google Gemini 3 Flash, a state-of-the-art large language model, reads the prompt and generates a natural, conversational answer grounded in the retrieved facts.

### Key Components
| Component            | File(s)                    | Responsibility                                              |
|----------------------|----------------------------|-------------------------------------------------------------|
| Web UI               | `frontend/components/`     | Chat interface, auth modal, sidebar, theme toggle           |
| API Server           | `api_wrapper.py`           | FastAPI REST API, auth middleware, request handling         |
| Query Engine         | `main.py`                  | Core RAG logic: embed, retrieve, filter, prompt, generate   |
| LLM Engine           | `gemini_engine.py`         | Wraps Google Gemini API for answer generation               |
| Embedding & Index    | `embed_and_index.py`       | E5-small-v2 embeddings, pgvector index building             |
| Data Loader          | `postgres_loader.py`       | Loads all PostgreSQL tables into LlamaIndex Documents       |
| DB Population Scripts| `database/*.py`            | Creates and populates domain tables in Supabase             |
| Configuration        | `config.py`                | Environment variable loading and Supabase config            |
| CLI Interface        | `main.py` (`main()` fn)    | Command-line chat interface for testing                     |

### Security
- All `/ask` API requests require a valid Supabase JWT bearer token.
- Tokens are verified live against the Supabase Auth API (not locally decoded), ensuring real-time revocation support.
- CORS is configured in FastAPI (currently open for development; should be restricted to the frontend origin in production).

### Logging
- `logs/system.log`: Records user logins, questions, and responses.
- `logs/retrieval_debug.log`: Records each retrieval query, chunk scores, and content for debugging retrieval quality.

---

## 13. Database

**Database Management System:** PostgreSQL 14+ (hosted on Supabase)
**Extension:** pgvector (for vector similarity search)
**Connection:** Supabase connection pooler (port 6543, SSL required)

The database contains seven tables:

| Table              | Type          | Purpose                                                      |
|--------------------|---------------|--------------------------------------------------------------|
| departments        | Domain data   | University departments                                       |
| faculty            | Domain data   | Faculty members with designations and department             |
| subjects           | Domain data   | Course subjects                                              |
| playlists          | Domain data   | YouTube playlist URLs for each subject                       |
| events             | Domain data   | Campus events with dates and locations                       |
| academic_calendar  | Domain data   | Academic year dates (fees, exams, holidays, semester start)  |
| documents          | Vector store  | Auto-generated embeddings for all domain records             |

The `documents` table is the backbone of the RAG system. It is populated automatically at server startup by `postgres_loader.py` (which reads all domain tables) and `embed_and_index.py` (which creates embeddings and writes to pgvector).

---

## 14. Table Description

### Table 1: departments
| Field           | Data Type     | Constraints            | Description                        |
|-----------------|---------------|------------------------|------------------------------------|
| department_id   | SERIAL        | PRIMARY KEY            | Auto-incremented unique identifier |
| department_name | TEXT          | UNIQUE, NOT NULL       | Name of the university department  |

**Sample Data:**
- Department of Computer Science & Engineering
- Department of Economics
- Department of Journalism and Mass Communication
- Department of Languages, Literatures and Cultural Studies
- Department of Arts

---

### Table 2: faculty
| Field           | Data Type     | Constraints                          | Description                          |
|-----------------|---------------|--------------------------------------|--------------------------------------|
| faculty_id      | SERIAL        | PRIMARY KEY                          | Auto-incremented unique identifier   |
| name            | TEXT          | NOT NULL                             | Full name of the faculty member      |
| designation     | TEXT          | NOT NULL                             | Academic designation/rank            |
| department_id   | INTEGER       | FOREIGN KEY → departments(department_id) ON DELETE CASCADE | Department affiliation |

**Designations included:** Professor, Associate Professor, Assistant Professor (Scale I, II, III), Senior Faculty

---

### Table 3: subjects
| Field           | Data Type     | Constraints            | Description                          |
|-----------------|---------------|------------------------|--------------------------------------|
| subject_id      | SERIAL        | PRIMARY KEY            | Auto-incremented unique identifier   |
| subject_name    | TEXT          | UNIQUE, NOT NULL       | Name of the course subject           |

**Sample Data:** DAA, DSA, Operating System, Automata and Compiler Design, Java OOPs

---

### Table 4: playlists
| Field           | Data Type     | Constraints                                          | Description                           |
|-----------------|---------------|------------------------------------------------------|---------------------------------------|
| playlist_id     | SERIAL        | PRIMARY KEY                                          | Auto-incremented unique identifier    |
| subject_id      | INTEGER       | FOREIGN KEY → subjects(subject_id) ON DELETE CASCADE | Associated subject                    |
| url             | TEXT          | NOT NULL                                             | YouTube playlist URL for the subject  |

Each subject has 2 or more associated playlist URLs.

---

### Table 5: events
| Field           | Data Type     | Constraints            | Description                          |
|-----------------|---------------|------------------------|--------------------------------------|
| id              | INTEGER       | PRIMARY KEY            | Unique event identifier              |
| title           | TEXT          | NOT NULL               | Name of the event                    |
| description     | TEXT          |                        | Description of the event             |
| event_date      | TEXT          |                        | Date or date range of the event      |
| location        | TEXT          |                        | Venue of the event                   |

**Sample Events:** #include (Feb 2025), ACM ROCS (Nov 2024), International Symposium for Data Science (Nov 2024), Elicit'24 Techno Cultural Fest (Sep 2024), Job Junction (Apr 2024)

---

### Table 6: academic_calendar
| Field           | Data Type     | Constraints            | Description                              |
|-----------------|---------------|------------------------|------------------------------------------|
| id              | INTEGER       | PRIMARY KEY            | Unique academic event identifier         |
| title           | TEXT          | NOT NULL               | Name of the academic event               |
| start_date      | TEXT          |                        | Start date of the event                  |
| end_date        | TEXT          |                        | End date of the event                    |
| description     | TEXT          |                        | Description of the academic calendar event |

**Sample Events:** Fee payment portal opening (Jun 2023), PhD Entrance Examination (Jul 2023), Commencement of classes (Jul 2023), Mid Terms (Mar 2024), End Terms (May 2024)

---

### Table 7: documents (Auto-populated)
| Field           | Data Type        | Constraints    | Description                                      |
|-----------------|------------------|----------------|--------------------------------------------------|
| id              | BIGSERIAL        | PRIMARY KEY    | Auto-incremented unique identifier               |
| content         | TEXT             |                | Text representation of the original record      |
| embedding       | vector(384)      |                | E5-small-v2 vector embedding (384 dimensions)   |
| metadata        | JSONB            |                | Source table name and other metadata            |
| created_at      | TIMESTAMP        |                | Time of embedding creation                      |

---

## 15. File / Database Design

### Project File Structure
```
AskQuery/
├── main.py                   # Core RAG logic + CLI interface
├── api_wrapper.py            # FastAPI backend server
├── gemini_engine.py          # Google Gemini LLM wrapper
├── embed_and_index.py        # E5-small-v2 embeddings + pgvector index builder
├── postgres_loader.py        # Loads all PostgreSQL tables into LlamaIndex Documents
├── config.py                 # Environment variable loading and Supabase config
├── requirements.txt          # Python dependency list
├── start.sh                  # Production startup script (uvicorn)
├── .env                      # Environment variables (not committed)
├── database/
│   ├── cse.py                # Populates CSE department and faculty
│   ├── department_faculty.py # Populates other departments and faculty
│   ├── subjects_playlist.py  # Populates subjects and playlists
│   └── events_academic_events.py # Populates events and academic calendar
├── logs/
│   ├── system.log            # Application-level logs (queries, responses, errors)
│   └── retrieval_debug.log   # Per-query retrieval chunk details and scores
└── frontend/
    ├── app/
    │   ├── page.tsx           # Root page component (renders AIAssistantUI)
    │   ├── layout.tsx         # Root layout (metadata, fonts, AuthProvider, Analytics)
    │   └── globals.css        # Global styles and Tailwind directives
    ├── components/
    │   ├── AIAssistantUI.jsx  # Top-level UI orchestrator (state, routing, auth)
    │   ├── AuthModal.jsx      # Login and signup form backed by Supabase Auth
    │   ├── AuthProvider.jsx   # React context for auth state and Supabase client
    │   ├── ChatPane.jsx       # Message history + composer for active conversation
    │   ├── Composer.jsx       # Text input area for typing queries
    │   ├── Message.jsx        # Individual message bubble component
    │   ├── Sidebar.jsx        # Conversation list, search, pin, collapse
    │   ├── Header.jsx         # Top navigation bar
    │   ├── ThemeToggle.jsx    # Light/dark mode switch
    │   ├── Sidebar*.jsx       # Sidebar sub-components
    │   └── ui/                # Radix UI-based reusable UI primitives
    ├── lib/
    │   └── api.js             # Frontend API service (healthCheck, askQuestion)
    ├── hooks/                 # Custom React hooks
    ├── public/                # Static assets (icon.svg, etc.)
    ├── package.json           # Node.js dependencies
    ├── next.config.mjs        # Next.js configuration
    └── tsconfig.json          # TypeScript configuration
```

### Database Design Summary
- **Schema**: All tables reside in the `public` schema of the Supabase PostgreSQL database.
- **Vector Dimension**: 384 (E5-small-v2 model output size).
- **Foreign Key Constraints**: faculty.department_id → departments.department_id; playlists.subject_id → subjects.subject_id (both with ON DELETE CASCADE).
- **Index**: pgvector automatically creates an index on the `embedding` column for approximate nearest neighbor (ANN) search.
- **Connection Pooling**: Supabase connection pooler (port 6543) is used for efficient connection management.

---

## 16. Input / Output Form Design

### 16.1 Authentication Form (AuthModal)

**Input Fields:**
| Field      | Type     | Validation                           | Description                        |
|------------|----------|--------------------------------------|------------------------------------|
| Username   | Text     | Required, valid email format         | User's email address (used as ID)  |
| Password   | Password | Required, minimum 6 characters       | User's password                    |

**Action Buttons:**
- **Login** — Authenticates the user against Supabase Auth.
- **Sign Up** — Creates a new account in Supabase Auth.
- **Toggle** — Switches between Login and Sign Up modes.

**Output:**
- On success: Modal closes, user enters the main chat interface. JWT token stored in session.
- On error: Inline error message displayed below the form (e.g., "Invalid credentials", "Backend server not running").
- On signup success: Confirmation message shown; user redirected to login.

---

### 16.2 Chat Interface (ChatPane + Composer)

**Input:**
| Field           | Type     | Description                                              |
|-----------------|----------|----------------------------------------------------------|
| Message Input   | Textarea | User types a natural language question (multi-line)      |
| Send Button     | Button   | Submits the question to the backend API                  |
| Edit Button     | Icon     | Allows editing a previously sent message                 |
| Resend Button   | Icon     | Resends a message (triggers a new API call)              |

**Output:**
| Element          | Description                                              |
|------------------|----------------------------------------------------------|
| User Bubble      | Right-aligned dark bubble showing the user's question   |
| AI Bubble        | Left-aligned light bubble showing the AI's answer        |
| Thinking Indicator | Animated bouncing dots while the AI is processing     |
| Pause Button     | Allows cancelling a pending response                     |

**Example Interaction:**

```
User: Who are the assistant professors in the Economics department?

AI:  The Economics department has the following Assistant Professors:
     Dr. [Name], Assistant Professor (Scale II); Dr. [Name], Assistant
     Professor; and Dr. [Name], Assistant Professor (Scale I).
```

---

### 16.3 Sidebar (Conversation Management)

| Element             | Input/Output | Description                                       |
|---------------------|--------------|---------------------------------------------------|
| Search bar          | Input        | Filter conversations by title or preview text     |
| New Chat button     | Input        | Creates a new conversation thread                 |
| Conversation list   | Output       | Shows all conversations sorted by last updated    |
| Pin/Unpin           | Input        | Toggle pin status of a conversation               |
| Collapse/Expand     | Input        | Collapse the sidebar to maximize chat area        |
| Username display    | Output       | Shows logged-in user's email                      |
| Logout button       | Input        | Signs out and clears local conversation data      |

---

## 17. Testing & Tools Used

### 17.1 Testing Approach

**1. Manual Functional Testing**
The primary testing method used is manual end-to-end testing of user-facing functionality:
- Login and signup via Supabase Auth
- Submitting questions and verifying responses
- Edge cases: empty questions, very long questions, questions with no relevant data
- Theme switching (light/dark)
- Sidebar operations (create, pin, search, collapse)

**2. API Endpoint Testing**
Backend endpoints were tested manually using:
- **Browser**: Visiting `http://127.0.0.1:8000/health` to verify server status.
- **curl / HTTP clients**: Testing the `/ask` endpoint with and without valid JWT tokens.

Example `/ask` request:
```http
POST http://127.0.0.1:8000/ask
Authorization: Bearer <supabase_jwt_token>
Content-Type: application/json

{
  "question": "Which departments does the university have?"
}
```

**3. Retrieval Quality Testing**
The `logs/retrieval_debug.log` file is used to inspect retrieval performance:
- Chunk scores and relevance for each query
- Number of chunks retrieved above/below the threshold
- Most relevant database table inferred per query

**4. CLI Interface Testing**
`main.py` includes a command-line chat interface that allows testing the full RAG pipeline without the frontend:
```bash
python main.py
# Choose: 1 (Login) or 2 (Signup)
# Enter credentials
# Type your question
```

### 17.2 Tools Used

| Tool/Technology         | Purpose                                                       |
|-------------------------|---------------------------------------------------------------|
| FastAPI (Swagger UI)    | Auto-generated API docs at `http://127.0.0.1:8000/docs`      |
| Supabase Dashboard      | Database inspection, SQL editor, auth user management         |
| Python logging module   | System and retrieval debug logging                            |
| Browser DevTools        | Frontend debugging (console, network, localStorage)           |
| Git / GitHub            | Version control and code hosting                              |
| Vercel                  | Frontend deployment and preview URLs                          |
| Google AI Studio        | Gemini API key management and model testing                   |

---

## 18. Implementation & Maintenance

### 18.1 Implementation

**Phase 1 — Database Setup**
1. Create a Supabase project and enable the pgvector extension.
2. Run database population scripts to create and populate domain tables:
   - `python database/cse.py`
   - `python database/department_faculty.py`
   - `python database/subjects_playlist.py`
   - `python database/events_academic_events.py`

**Phase 2 — Backend Deployment**
1. Install Python dependencies: `pip install -r requirements.txt`
2. Configure `.env` with Gemini API key and Supabase credentials.
3. Start the FastAPI server:
   - Development: `python api_wrapper.py`
   - Production: `./start.sh` (uses uvicorn on port from `$PORT` env variable)
4. On first startup, the backend automatically builds the pgvector index (1–3 minutes for first run; subsequent startups load from the existing database).

**Phase 3 — Frontend Deployment**
1. Navigate to `frontend/`.
2. Create `.env.local` with `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SUPABASE_URL`, and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
3. Install dependencies: `pnpm install` or `npm install`.
4. Development server: `pnpm dev` → runs at `http://localhost:3000`.
5. Production build: `pnpm build && pnpm start` or deploy to Vercel (connects the GitHub repo and auto-deploys on push).

### 18.2 Maintenance

**Adding New Data:**
- New university data can be added by writing a new script in `database/` that inserts records into the relevant table (or creates a new table if needed).
- After adding data, restart the backend so the vector index is rebuilt to include the new records.

**Updating the LLM:**
- The Gemini model is configured in `gemini_engine.py`. Switching to a newer Gemini model requires only changing the model string (`"gemini-3-flash-preview"`).

**Monitoring:**
- `logs/system.log` — Review for errors, user activity, and response quality.
- `logs/retrieval_debug.log` — Review to tune `similarity_top_k` and `similarity_cutoff` parameters in `main.py`.

**Dependency Updates:**
- Backend: `pip install --upgrade -r requirements.txt`
- Frontend: `pnpm upgrade`

**Scaling:**
- The backend can be scaled horizontally (multiple uvicorn workers) since all state is stored in Supabase.
- The frontend is stateless (conversations stored in `localStorage`) and scales trivially on Vercel's CDN.

---

## 19. Conclusion and Future Work

### Conclusion

AskQuery successfully demonstrates the practical application of Retrieval-Augmented Generation (RAG) technology to solve a real-world institutional challenge: making university data accessible to everyone through natural language. The system achieves:

- **Accuracy**: By grounding LLM responses in actual database records rather than model memory, hallucination is minimized and answers are factually reliable.
- **Accessibility**: Students no longer need SQL knowledge or database access to retrieve institutional information — any plain English question works.
- **Security**: Supabase JWT authentication ensures only authorized users can query the system.
- **Performance**: The use of E5-small-v2 (a lightweight 384-dim embedding model) makes the system fully CPU-compatible, reducing infrastructure costs.
- **Modern UX**: The Next.js frontend provides a responsive, polished chat experience comparable to commercial AI assistants.

The project validates that RAG-based architectures can be cost-effectively applied to domain-specific institutional data, even with relatively small databases.

### Future Work

1. **Expanded Knowledge Base**: Add more university data — hostel information, fee structures, library catalog, course syllabi, faculty research publications.
2. **Multi-turn Conversation**: Implement conversation history in prompts so the AI can understand follow-up questions referring to previous answers ("Which ones are in CSE?" after asking about professors).
3. **Voice Input/Output**: Integrate speech-to-text and text-to-speech APIs for accessibility and hands-free queries.
4. **Admin Panel**: Build an admin interface for non-technical university staff to upload and update data without writing scripts.
5. **Analytics Dashboard**: Surface query statistics — most common questions, average response times, retrieval quality metrics — for administrators.
6. **Advanced Retrieval**: Implement hybrid search (combining BM25 keyword search with vector similarity) for better precision on entity-heavy queries (e.g., specific person names).
7. **Fine-tuned Embeddings**: Fine-tune the embedding model on university domain text to improve retrieval relevance.
8. **Mobile Application**: Develop a React Native or Flutter mobile app backed by the same FastAPI server.
9. **Multi-language Support**: Add Hindi-language query support to make the system accessible to a wider user base.
10. **Production Hardening**: Restrict CORS to the production frontend domain, implement rate limiting, and add proper SSL termination.

---

## 20. Outcome

**Deployment-based Outcome:**
AskQuery has been successfully developed and is ready for deployment. The backend is hosted as a FastAPI service (deployable to cloud platforms such as Render, Railway, or a VPS using the provided `start.sh` script), while the frontend is deployable to Vercel with a single GitHub integration. The system is fully functional end-to-end, allowing authenticated university users to submit natural language queries and receive AI-generated answers sourced from the live PostgreSQL database — demonstrating a complete, production-grade implementation of a RAG-based institutional assistant.

*(The project is at the deployment stage of completion. Further work toward a research paper submission, copyright registration, or patent filing is planned as the system is extended with multi-turn conversation and advanced retrieval capabilities.)*

---

## 21. Bibliography

1. **LlamaIndex Documentation** — "Building RAG Pipelines with LlamaIndex." Available at: https://docs.llamaindex.ai/
2. **FastAPI Documentation** — "FastAPI: Modern, fast web framework for building APIs with Python." Available at: https://fastapi.tiangolo.com/
3. **Google Gemini API Documentation** — "Google Generative AI (Gemini) for Developers." Available at: https://ai.google.dev/
4. **Supabase Documentation** — "Supabase: The Open Source Firebase Alternative." Available at: https://supabase.com/docs
5. **pgvector GitHub** — "pgvector: Open-source vector similarity search for Postgres." Available at: https://github.com/pgvector/pgvector
6. **Hugging Face — intfloat/e5-small-v2** — "Text Embeddings by Weakly-Supervised Contrastive Pre-training." Available at: https://huggingface.co/intfloat/e5-small-v2
7. **Next.js Documentation** — "The React Framework for Production." Available at: https://nextjs.org/docs
8. **Tailwind CSS Documentation** — "A utility-first CSS framework." Available at: https://tailwindcss.com/docs
9. **Radix UI Documentation** — "Unstyled, accessible components for building high-quality design systems." Available at: https://www.radix-ui.com/
10. **Manipal University Jaipur** — Official university website. Available at: https://jaipur.manipal.edu/
11. **Lewis, P., et al. (2020)** — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *arXiv:2005.11401*. Available at: https://arxiv.org/abs/2005.11401
12. **Wang, L., et al. (2022)** — "Text Embeddings by Weakly-Supervised Contrastive Pre-training." *arXiv:2212.03533*. Available at: https://arxiv.org/abs/2212.03533
13. **Python Software Foundation** — "Python 3 Documentation." Available at: https://docs.python.org/3/
14. **PostgreSQL Global Development Group** — "PostgreSQL 14 Documentation." Available at: https://www.postgresql.org/docs/14/
15. **GitHub Repository** — "srivastavaprakhar/AskQuery." Available at: https://github.com/srivastavaprakhar/AskQuery
