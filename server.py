"""
LangServe Entry Point
---------------------
Starts a FastAPI application and mounts the AI Career Agent
at multiple LangServe routes.

Endpoints exposed:
  POST /career-agent/invoke          — single-turn invocation
  POST /career-agent/stream          — streaming response
  POST /career-agent/batch           — batch invocation
  GET  /career-agent/playground      — LangServe interactive UI

  POST /tools/resume-analyzer/invoke — direct resume analysis
  POST /tools/jd-matcher/invoke      — direct JD matching
  POST /tools/interview-prep/invoke  — direct interview prep
  POST /tools/career-roadmap/invoke  — direct roadmap generation
  POST /tools/cover-letter/invoke    — direct cover letter generation

  GET  /health                       — health check (used by Render)
  GET  /                             — API info page
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from app.agent import create_career_agent_with_history
from app.tools import (
    resume_analyzer_tool,
    jd_matcher_tool,
    interview_prep_tool,
    career_roadmap_tool,
    cover_letter_tool,
)

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

# Fail fast if the OpenAI key is not set
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. "
        "Add it to your .env file or Render environment variables."
    )

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 AI Career Agent is starting up...")
    yield
    print("🛑 AI Career Agent is shutting down...")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI Career Agent",
    description=(
        "A placement-ready AI Career Agent powered by LangChain 1.x and LangServe. "
        "Provides resume analysis, JD matching, interview prep, career roadmaps, "
        "and cover letter generation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for playground / testing.
# Restrict in production by setting ALLOWED_ORIGINS env var.
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health check (Render uses this to verify the service is healthy)
# ---------------------------------------------------------------------------

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "ai-career-agent"}


@app.get("/", tags=["System"])
async def root():
    return RedirectResponse(url="/docs")


# ---------------------------------------------------------------------------
# Main agent route (with per-session message history)
# ---------------------------------------------------------------------------

add_routes(
    app,
    create_career_agent_with_history(),
    path="/career-agent",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="default",
)

# ---------------------------------------------------------------------------
# Individual tool routes (stateless, direct access)
# ---------------------------------------------------------------------------

# Wrap each @tool as a RunnableLambda so LangServe can mount it
def _tool_runnable(tool_fn):
    """Convert a LangChain @tool into a Runnable that LangServe can mount."""
    return RunnableLambda(lambda x: tool_fn.invoke(x.get("input", x)))


add_routes(app, _tool_runnable(resume_analyzer_tool), path="/tools/resume-analyzer")
add_routes(app, _tool_runnable(jd_matcher_tool),      path="/tools/jd-matcher")
add_routes(app, _tool_runnable(interview_prep_tool),   path="/tools/interview-prep")
add_routes(app, _tool_runnable(career_roadmap_tool),   path="/tools/career-roadmap")
add_routes(app, _tool_runnable(cover_letter_tool),     path="/tools/cover-letter")

# ---------------------------------------------------------------------------
# Run directly (for local development)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
