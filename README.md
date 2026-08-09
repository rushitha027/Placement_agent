# 🤖 AI Career Agent

A **placement-ready AI Career Agent** built with **LangChain 1.x** and served via **LangServe** on **Render**.

The agent helps job seekers with every step of their placement journey — resume review, JD matching, interview preparation, career roadmaps, and cover letter generation — all through a single conversational AI interface.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📋 **Resume Analyzer** | ATS score, strengths, gaps, and actionable improvement tips |
| 🎯 **JD Matcher** | Match % between your resume and a job description + tailoring advice |
| 🧠 **Interview Prep** | Role-specific questions with model answers (technical + behavioral) |
| 🗺️ **Career Roadmap** | Time-bound, personalised career plan from your current role to target |
| ✉️ **Cover Letter Generator** | Tailored, professional cover letters ready to send |

---

## 🏗️ Project Structure

```
ai-career-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py          # AgentExecutor + session history
│   ├── server.py         # FastAPI + LangServe entry point
│   └── tools/
│       ├── __init__.py
│       ├── resume_analyzer.py
│       ├── jd_matcher.py
│       ├── interview_prep.py
│       ├── career_roadmap.py
│       └── cover_letter.py
├── requirements.txt
├── Procfile              # Render start command
├── render.yaml           # Render IaC config
├── .env.example          # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1. Clone & set up environment

```bash
git clone <your-repo-url>
cd ai-career-agent

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the server

```bash
uvicorn app.server:app --reload --port 8000
```

Open **http://localhost:8000/docs** for the Swagger UI.  
Open **http://localhost:8000/career-agent/playground** for the LangServe playground.

---

## 🌐 API Endpoints

### Agent (multi-turn conversation)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/career-agent/invoke` | Single-turn invocation |
| `POST` | `/career-agent/stream` | Streaming response |
| `POST` | `/career-agent/batch` | Batch invocation |
| `GET`  | `/career-agent/playground` | Interactive LangServe UI |

**Request body:**
```json
{
  "input": {
    "input": "Analyze my resume and tell me how to improve it for a Data Engineer role.",
    "chat_history": []
  },
  "config": {
    "configurable": { "session_id": "user-123" }
  }
}
```

### Direct Tool Endpoints (stateless)

| Method | Path | Tool |
|--------|------|------|
| `POST` | `/tools/resume-analyzer/invoke` | Resume Analyzer |
| `POST` | `/tools/jd-matcher/invoke` | JD Matcher |
| `POST` | `/tools/interview-prep/invoke` | Interview Prep |
| `POST` | `/tools/career-roadmap/invoke` | Career Roadmap |
| `POST` | `/tools/cover-letter/invoke` | Cover Letter |

**Request body for direct tools:**
```json
{
  "input": {
    "input": "ROLE: Machine Learning Engineer\nCOMPANY: Google\nEXPERIENCE_LEVEL: junior\nFOCUS_AREAS: Python, TensorFlow, MLOps"
  }
}
```

### System

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check (used by Render) |
| `GET` | `/` | Redirects to `/docs` |

---

## ☁️ Deploy to Render

### Option A — Using `render.yaml` (recommended)

1. Push the repo to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your GitHub repo — Render will auto-detect `render.yaml`.
4. Set the `OPENAI_API_KEY` secret in the Render dashboard under **Environment**.
5. Click **Deploy**.

### Option B — Manual Web Service

1. New → Web Service → connect repo.
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `uvicorn app.server:app --host 0.0.0.0 --port $PORT`
4. Add `OPENAI_API_KEY` in Environment Variables.
5. Deploy.

> **Note:** The free Render plan spins down after 15 minutes of inactivity. Upgrade to the Starter plan for always-on availability.

---

## 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | — | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-3.5-turbo` | OpenAI model to use |
| `AGENT_TEMPERATURE` | No | `0.3` | LLM temperature (0–1) |
| `PORT` | No | `8000` | Server port (set by Render automatically) |
| `ALLOWED_ORIGINS` | No | `*` | CORS allowed origins |
| `LANGCHAIN_TRACING_V2` | No | — | Enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | — | LangSmith API key |

---

## 🧪 Example Tool Inputs

### Resume Analyzer
```
RESUME:
John Doe | john@email.com | linkedin.com/in/johndoe
Skills: Python, SQL, Pandas, Tableau
Experience: Data Analyst at XYZ Corp (2 years)
Education: B.Tech Computer Science

TARGET_ROLE: Data Engineer
```

### JD Matcher
```
RESUME:
<paste resume here>

JOB_DESCRIPTION:
We are looking for a Backend Engineer with 2+ years of experience in Python,
FastAPI, PostgreSQL, Docker, and AWS...
```

### Career Roadmap
```
CURRENT_ROLE: fresher
TARGET_ROLE: Machine Learning Engineer
CURRENT_SKILLS: Python, basic statistics, pandas
EDUCATION: B.Tech Computer Science
TIMELINE: 12 months
```

---

## 🛠️ Tech Stack

- **LangChain** 0.1.20 — Agent framework
- **LangChain OpenAI** 0.1.8 — OpenAI integration
- **LangServe** 0.1.0 — REST API layer
- **FastAPI** 0.111.0 — Web framework
- **Uvicorn** 0.30.1 — ASGI server
- **OpenAI GPT-3.5-Turbo** — Underlying LLM

---

## 📄 License

MIT
