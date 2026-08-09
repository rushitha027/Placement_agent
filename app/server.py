import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from app.agent import create_career_agent_with_history
from app.tools import (resume_analyzer_tool, jd_matcher_tool,
                        interview_prep_tool, career_roadmap_tool, cover_letter_tool)

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY is not set.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AI Career Agent starting...")
    yield

app = FastAPI(title="AI Career Agent", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "healthy"}

@app.get("/")
async def root(): return RedirectResponse(url="/docs")

add_routes(app, create_career_agent_with_history(), path="/career-agent",
           enable_feedback_endpoint=True, enable_public_trace_link_endpoint=True)

def _wrap(tool_fn): return RunnableLambda(lambda x: tool_fn.invoke(x.get("input", x)))

add_routes(app, _wrap(resume_analyzer_tool), path="/tools/resume-analyzer")
add_routes(app, _wrap(jd_matcher_tool),      path="/tools/jd-matcher")
add_routes(app, _wrap(interview_prep_tool),   path="/tools/interview-prep")
add_routes(app, _wrap(career_roadmap_tool),   path="/tools/career-roadmap")
add_routes(app, _wrap(cover_letter_tool),     path="/tools/cover-letter")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
