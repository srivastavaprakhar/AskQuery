# AskQuery

A lightweight RAG-based assistant that helps students query university databases in natural language. AskQuery integrates modern retrieval and generation techniques, enabling efficient, accurate answers on low-resource devices.

## Features

- **Natural Language Querying**: Students can ask questions in plain English.
- **RAG Architecture**: Combines Retrieval Augmented Generation for relevant, concise responses.
- **Storage**: Uses SQLite (relational) and FAISS (vector) databases for efficient data management and search.
- **Embeddings**: Employs MiniLM/E5 for fast, high-quality retrieval.
- **CPU-Friendly LLM**: Mistral 7B (GGUF format) for concise answers, optimized for local, low-resource hardware.
- **Low Resource Optimizations**: Designed for laptops and devices without GPUs.
- **Simple Web UI**: Interact via a clean browser interface.

## Tech Stack

- **Backend**: Python (FastAPI) with RAG pipeline
- **Frontend**: Next.js (React) with TypeScript
- **Database**: SQLite (relational) and FAISS (vector)
- **LLM**: Mistral 7B (GGUF format) via Shivaay Engine
- **Embeddings**: MiniLM/E5 for fast retrieval

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher (for frontend)
- pnpm or npm (package manager)

### Backend Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/srivastavaprakhar/AskQuery.git
   cd AskQuery
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the model path** (if needed)
   - Update `MODEL_PATH` in `config.py` to point to your Mistral model file
   - Ensure the model file exists at the specified path

4. **Setup environment variables** (optional)
   - Create a `.env` file if using Shivaay API
   - Add `SHIVAAY_API_KEY=your_api_key` if needed

5. **Run the backend server**
   ```bash
   python api_wrapper.py
   ```
   - The backend API will start at `http://127.0.0.1:8000`
   - The server will initialize the model and build the FAISS index on startup

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Configure API URL** (optional)
   - Create a `.env.local` file in the `frontend` directory
   - Add `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` (default is already set)

4. **Run the frontend development server**
   ```bash
   npm run dev
   # or
   pnpm dev
   ```
   - The frontend will start at `http://localhost:3000`

### Running the Application

1. **Start the backend server** (in one terminal)
   ```bash
   python api_wrapper.py
   ```

2. **Start the frontend server** (in another terminal)
   ```bash
   cd frontend
   npm run dev
   # or
   pnpm dev
   ```

3. **Access the application**
   - Open your browser and navigate to `http://localhost:3000`
   - You will be prompted to sign up or login
   - After authentication, you can start asking questions

### API Endpoints

The backend provides the following API endpoints:

- `GET /health` - Health check endpoint
- `POST /signup` - User registration (requires `username` and `password`)
- `POST /login` - User authentication (requires `username` and `password`)
- `POST /ask` - Ask a question (requires `question` in request body)

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

- Ensure the model file exists at the path specified in `config.py`
- Check that you have enough disk space and memory
- The model file can be large (several GB), so initial load may take time

## Usage

- Query the database with questions like:
  > "Which all departments does the university consist of?"

- Responses are generated using the RAG pipeline for accuracy and context.

## Model Details

- **Embeddings**: [MiniLM/E5](https://huggingface.co/MiniLM)
- **LLM**: [Mistral 7B GGUF](https://github.com/mistralai/mistral-src)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
- **Relational DB**: [SQLite](https://www.sqlite.org/index.html)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

- [Mistral AI](https://mistral.ai/)
- [Facebook FAISS](https://github.com/facebookresearch/faiss)
- [Hugging Face](https://huggingface.co/)
