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

- **Python** (core logic & backend) 
- **CSS** (styling) 
- **JavaScript** (frontend interactions) 
- **HTML** (markup) 

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/srivastavaprakhar/AskQuery.git
   cd AskQuery
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup FAISS & MiniLM/E5**
   - Download or specify the MiniLM/E5 model.
   - Initialize FAISS index with your university database.

4. **Run the app**
   ```bash
   python app.py
   ```
   - Access the web UI at `http://localhost:8000`

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
