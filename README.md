# 🤖 Multimodal Research Assistant with LangGraph, Multi-Agent System, RAG, and MCP

An advanced AI-powered research assistant that uses **multi-agent architectures**, **LangGraph DAGs**, **Retrieval-Augmented Generation (RAG)**, and the **Multi-Context Protocol (MCP)** to search, summarize, and explain the latest research papers from sources like arXiv. The assistant handles **text, voice, and image inputs**, and supports **modular context passing** through MCP.

---

## 🚀 Features

- 🧠 **Multi-Agent Workflow** powered by [LangGraph](https://www.langgraph.dev)
- 📄 **Search & Summarization** of latest papers via arXiv, Semantic Scholar APIs
- 🗃️ **Retrieval-Augmented Generation (RAG)** with Chroma / FAISS
- 🔌 **Multi-Context Protocol (MCP)** for standardized context handling
- 🎤🖼️ **Multimodal Input Support** – Accepts text, audio (Whisper), and images (CLIP/GPT-4o)
- 🧩 **LLM Tools & Agents** for modular functionality (search, summarize, rank, respond)
- 🐳 **Dockerized**, CI/CD-ready with GitHub Actions
- 📊 **MLflow Tracking** and optional analytics

---

## 🧠 System Architecture

### 🕸️ LangGraph Multi-Agent Flow

```mermaid
graph TD
    A[Start: User Input] --> B{Input Classifier}
    B -->|Text| C[Controller Agent]
    B -->|Voice| D[Transcriber Agent (Whisper)]
    B -->|Image| E[Image Parser Agent]
    C --> F[Search Agent (ArxivTool)]
    F --> G[RAG Agent (Vector Search)]
    G --> H[Summarizer Agent]
    H --> I[Aggregator / Ranker Agent]
    I --> J[Final Response Generator]

##🔌 MCP Usage

Each agent reads/writes to a shared context object defined by the Multi-Context Protocol (MCP), enabling:

    Standard input/output contracts

    Reusability across LLM backends

    Easier plug-and-play agent development

🔧 Local Setup
# Clone repo
git clone https://github.com/sahana-github/Multi-Agent-Research-Assistant
cd multiagent-research-bot

# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend
uvicorn backend.main:app --reload

# Start frontend (optional)
streamlit run frontend/app.py

🐳 Docker (CI/CD Ready)

docker build -t research-bot .
docker run -p 8000:8000 research-bot

CI/CD Workflow

    ✅ GitHub Actions for linting, testing, build & deploy

    ✅ Dockerized backend for easy deployment (Render / HuggingFace)

    ✅ Automated LangGraph DAG validation on push

👩‍💻 Author

Sahana Durgekar
🔗 GitHub: @sahana-github
✉️ Email: 1ms20is407@gmail.com

