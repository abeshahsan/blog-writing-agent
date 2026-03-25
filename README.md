<h1 align="center">Blog Writing Agent</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-Web_API-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-FF6F00" alt="LangGraph" />
  <img src="https://img.shields.io/badge/LangChain-LLM_Framework-1C3C3C?logo=langchain&logoColor=white" alt="LangChain" />
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Ollama-Local_LLM-111111" alt="Ollama" />
  <img src="https://img.shields.io/badge/OpenRouter-Cloud_LLM-6D4AFF" alt="OpenRouter" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Pytest-Tested-0A9EDC?logo=pytest&logoColor=white" alt="Pytest" />
</p>

---

# Overview

This repository implements a topic-to-blog generation system with a graph-based pipeline and a simple browser UI.
A FastAPI backend accepts a topic, runs a multi-step LangGraph workflow, generates markdown content with an LLM, returns the markdown as a file response, and removes temporary files after sending.

The project supports two LLM operating modes:

- Local mode in development using Ollama.
- Cloud mode in test or production using OpenRouter.

The frontend is plain HTML, CSS, and JavaScript, and renders the returned markdown as scrollable HTML preview.

---

# Features

- Graph-based orchestration with orchestrator, worker fanout, and reducer nodes.
- Structured plan generation using Pydantic models for title and section tasks.
- Dual LLM routing by environment:
    - Development defaults to local Ollama model (`qwen2.5:3b`).
    - Test and production use OpenRouter cloud model.
- FastAPI endpoint (`POST /api/generate`) validates topic limits and returns markdown as file content.
- Temporary generated file cleanup after response send.
- Frontend includes:
    - Topic textbox
    - Character and word limits
    - Loading and error states
    - Markdown to HTML preview using `marked`
- Filename sanitization for Windows-safe markdown output names.
- Automated tests for graph nodes, LLM client behavior, markdown writer, blog service, and integration path.

---

# Architecture & Generation Pipeline

1. Request Intake
    - User submits topic from frontend UI.
2. API Validation
    - Backend validates max length and max word count.
3. Orchestration
    - Orchestrator creates a multi-section blog plan.
4. Section Generation
    - Worker node generates markdown for each section task.
5. Reduction
    - Reducer combines sections into final markdown and writes output file.
6. Delivery
    - API returns markdown file response, frontend reads response body, converts markdown to HTML, and shows it in preview.

```text
Browser UI
   |
   v
POST /api/generate -----------> FastAPI (app.py)
                                   |
                                   v
                           LangGraph Workflow
                      orchestrator -> worker(s) -> reducer
                                   |
                                   v
                         Markdown output written
                                   |
                                   v
                    FileResponse + background delete
                                   |
                                   v
                     Frontend markdown -> HTML preview
```

---

# CI Pipeline & Docker

This repo includes local CI-style scripts and Docker packaging.

Pipeline scripts:

- `pipeline.sh` for bash environments
- `pipeline.bat` for Windows

Pipeline flow:

1. Install dependencies including development extras.
2. Run test suite with pytest.
3. Build Docker image.

Docker runtime details:

- Base image: `python:3.12-slim`
- App server: Uvicorn (`app:app`)
- Exposed port: `8000`

---

# Installation

1. Clone repository

```bash
git clone https://github.com/abeshahsan/blog-writing-agent.git
cd blog-writing-agent
```

2. Create virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install package and dev dependencies

```bash
pip install -e .
pip install -e ".[dev]"
```

4. Configure environment files

- Ensure these files exist in project root:
    - `.env.development`
    - `.env.production`
    - `.env.test`

Cloud mode variables (used in test/production):

```env
OPENROUTER_API_KEY=...
OPENROUTER_BASE_URL=...
OPENROUTER_MODEL=...
```

---

# Usage

Run API locally:

```bash
# Default: development mode (local Ollama)
uvicorn app:app --reload
```

Open in browser:

- `http://127.0.0.1:8000`

Generate endpoint:

- `POST /api/generate`
- Request body:

```json
{
	"topic": "Self Attention in Transformers"
}
```

The response body is markdown content (sent as markdown file response) and frontend renders it to HTML.

Run CLI generation flow:

```bash
python main.py
```

---

# Local and Cloud LLM Modes

Mode selection is environment-driven:

- No `ENV_MODE` set: defaults to `development`.
- Explicit `ENV_MODE=production` or `ENV_MODE=test`: uses cloud OpenRouter client.

Mode behavior:

- Development:
    - Local provider via Ollama (`qwen2.5:3b`).
- Test/Production:
    - Cloud provider via OpenRouter (`langchain_openrouter`).

Examples:

```powershell
# Default local mode
Remove-Item Env:ENV_MODE -ErrorAction SilentlyContinue
uvicorn app:app --reload

# Cloud production mode
$env:ENV_MODE="production"
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

# Tech Stack

| Area                      | Stack                       | Badge                                                                                                |
| ------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------- |
| Language                  | Python 3.12                 | ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)               |
| API                       | FastAPI                     | ![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)             |
| App Server                | Uvicorn                     | ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-111111)                                         |
| Orchestration             | LangGraph                   | ![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-FF6F00)                                 |
| LLM Framework             | LangChain                   | ![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?logo=langchain&logoColor=white) |
| Local LLM                 | Ollama + ChatOllama         | ![Ollama](https://img.shields.io/badge/Ollama-Local_Model-111111)                                    |
| Cloud LLM                 | OpenRouter + ChatOpenRouter | ![OpenRouter](https://img.shields.io/badge/OpenRouter-Cloud_Model-6D4AFF)                            |
| Validation                | Pydantic v2                 | ![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063)                                         |
| Frontend                  | HTML, CSS, JavaScript       | ![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-F7DF1E)                            |
| Markdown Rendering        | marked.js                   | ![Marked](https://img.shields.io/badge/marked.js-Markdown_Render-4A4A4A)                             |
| Testing                   | Pytest                      | ![Pytest](https://img.shields.io/badge/Pytest-Tests-0A9EDC?logo=pytest&logoColor=white)              |
| Container                 | Docker                      | ![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)      |
| CI-style Local Automation | Bash + Batch scripts        | ![Pipeline](https://img.shields.io/badge/Local_Pipeline-sh%20%2B%20bat-555555)                       |

---

# Docker

Build image:

```bash
docker build -t blog-writing-agent .
```

Run container in production mode:

```bash
docker run --rm -p 8000:8000 -e ENV_MODE=production blog-writing-agent
```

---

# Testing

Run all tests:

```bash
pytest -q
```

Run a specific test module:

```bash
pytest tests/test_graph_nodes.py -q
```

---

# Project Structure

```text
blog-writing-agent/
├─ app.py
├─ main.py
├─ bootstrap.py
├─ setup.py
├─ Dockerfile
├─ pipeline.sh
├─ pipeline.bat
├─ frontend/
│  ├─ index.html
│  ├─ styles.css
│  └─ app.js
├─ blog_writing_agent/
│  ├─ config.py
│  ├─ exceptions.py
│  ├─ logging_utils.py
│  ├─ graph/
│  │  ├─ nodes.py
│  │  └─ wiring.py
│  ├─ io/
│  │  └─ markdown_writer.py
│  ├─ llm/
│  │  ├─ client.py
│  │  ├─ local_llm.py
│  │  └─ cloud_llm.py
│  ├─ models/
│  │  ├─ plan.py
│  │  └─ state.py
│  └─ services/
│     └─ blog_service.py
└─ tests/
   ├─ test_blog_service.py
   ├─ test_graph_nodes.py
   ├─ test_llm_client.py
   ├─ test_markdown_writer.py
   └─ integration/
      └─ test_pipeline_integration.py
```

---

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# Contributing

1. Create a feature branch.
2. Keep pull requests focused and add tests for new behavior.
3. Verify local run and pipeline scripts before opening a PR.
4. Include concise technical notes in the PR description.
