# AI-Assist-2
A chatbot on Llama with RAG and prompt engineering.


# Company AI Assist (Local LLaMA + RAG + prompt enginnering)

## Overview

This project is a **local, cost‑free AI assistant** designed to answer questions about a company, its products, clients, services, and internal references.

It uses:

* A **local open‑source LLM** (TinyLLaMA / LLaMA‑family via `llama-cpp`)
* A **Retrieval‑Augmented Generation (RAG)** pipeline
* A **SQLite‑based vector database** for company knowledge
* A **FastAPI backend**
* A **minimal web chat UI** (HTML/CSS/JS)

The system is intended primarily for **local experimentation, prototyping, and internal demos**, not high‑performance production use as thatwill need a cloud server and will entail costs.

---

## High‑Level Architecture

```
User (Browser)
   │
   ▼
Web UI (HTML / JS)
   │   POST /chat
   ▼
FastAPI Backend
   │
   ├─ RAG Pipeline
   │    ├─ Embed user query
   │    ├─ Retrieve relevant company data (SQLite)
   │    └─ Build constrained prompt
   │
   └─ Local LLM (llama‑cpp)
        └─ Generates final answer
```

---

## Repository Structure

```
ai-assist-2/
├── backend/
│   ├── __init__.py
│   ├── app.py          # FastAPI server & routes
│   ├── rag.py          # RAG logic (retrieve + prompt)
│   ├── llm.py          # Local LLM loading & inference
│   ├── embeddings.py  # Embedding + SQLite vector search
│   └── config.py      # Central configuration
│   └── requirements.txt
│
├── frontend/
│   ├── index.html     # Chat UI
│   ├── style.css      # Minimal styling
│   ├── app.js         # Browser-side logic
│   ├── assistant.jpg  # Assistant avatar
│   └── favicon.ico    # Optional favicon
│
├── data/
│   ├── raw/           # Company data (txt / md files)
│   └── vectors.db     # SQLite vector database (auto-created)
│
├── models/            # Local GGUF LLM files (not in Git)
│
├── scripts/
│   └── ingest.py      # Builds the vector database
│
└── README.md
```

---

## Module Responsibilities

### `backend/app.py`

* Starts the FastAPI application
* Serves the frontend (`/`)
* Serves static files (`/static/*`)
* Exposes the `/chat` API endpoint

### `backend/rag.py`

* Retrieves relevant text chunks from SQLite
* Builds a **strict prompt** optimized for small models
* Calls the LLM to generate the answer

### `backend/llm.py`

* Loads the local GGUF model (we used tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf for its lightness and speed on local machine) via `llama-cpp-python`
* Controls inference parameters (context size, tokens, temperature)

### `backend/embeddings.py`

* Uses `sentence-transformers` for embeddings
* Stores vectors in SQLite
* Performs cosine similarity search

### `scripts/ingest.py`

* Reads company data files
* Embeds and stores them in `vectors.db`
* Run once (or whenever data changes)

### `frontend/*`

* Minimal chat UI
* Sends user questions to `/chat`
* Displays assistant responses

---

## Data Format (Important)

Company knowledge should be stored as **plain text files** in `data/raw/`. 

Best practices:

* One file per topic (products, clients, services, etc.)
* Short, factual paragraphs
* Avoid large unstructured documents

Example:

```
Product: Smart Lift Manipulator
Description: A robotic lifting and positioning system used in industrial inspection.
```

This structure improves embedding quality and retrieval accuracy.

---

## Model Choice

### Local Development Model

Recommended for my hardware (Intel i7 / 16GB RAM):

* **TinyLLaMA‑1.1B‑Chat (Q4 GGUF)**

Why:

* Runs locally without crashing
* Much faster than 7B+ models
* Good enough for fact‑based Q&A with RAG

Trade‑offs:

* Limited reasoning
* Short answers only
* Relies heavily on retrieved context

The model file is **not included in the repository** and must be downloaded separately.

---

## Setup Instructions

### 1. Create a virtual environment (Python 3.10 recommended)

```bash
python3.10 -m venv ai_assist_env
source ai_assist_env/bin/activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn llama-cpp-python sentence-transformers sqlite-utils pydantic "numpy<2"
```

### 3. Download a GGUF model

Place the model file in:

```
models/
```

Update `backend/config.py` to match the filename.

---

## Build the Knowledge Base

Add your company data to:

```
data/raw/
```

Then run:

```bash
python scripts/ingest.py
```

This creates:

```
data/vectors.db
```

---

## Running the Application

From the project root:

```bash
uvicorn backend.app:app --reload
```

Then open:

```
http://127.0.0.1:8000/
```

The `/docs` endpoint is available for API testing but not required for normal use.

---

## Performance Notes

* First query can take **many minutes** on limited hardware
* Subsequent queries are faster
* This is expected for local CPU‑based inference

This project prioritizes:

* Transparency
* Zero cloud cost
* Full local control

Not speed.

However, if you use the code on an advanced computer with plenty of CPUs and GPUs you'll experience a much faster performance and you might even want to use heavier 7B or 8B Llamma models.
---

## Limitations

* Not suitable for production traffic
* No authentication
* No multi‑user memory
* No streaming responses
* Limited reasoning ability (small model)

---

## When to Stop Here

This setup is ideal if you want:

* A working local AI assistant
* A learning / prototype system
* A privacy‑preserving demo

For real deployment, a dedicated server or managed inference service is recommended.

---

## License

Open‑source components are used under their respective licenses.
Company data and usage policies remain the responsibility of the user.
