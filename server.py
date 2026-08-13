import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.tools import (
    resume_analyzer_tool, jd_matcher_tool, interview_prep_tool,
    career_roadmap_tool, cover_letter_tool,
)

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY is not set.")

TOOLS = [resume_analyzer_tool, jd_matcher_tool, interview_prep_tool,
         career_roadmap_tool, cover_letter_tool]

SYSTEM_PROMPT = """You are an elite AI Career Agent helping job seekers land placements.
You have access to these tools:
1. resume_analyzer_tool - resume review with ATS score
2. jd_matcher_tool - resume vs JD fit analysis
3. interview_prep_tool - interview questions with answers
4. career_roadmap_tool - personalised career plan
5. cover_letter_tool - professional cover letter
Always pick the right tool and summarise after each response."""

def create_agent():
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                     temperature=float(os.getenv("AGENT_TEMPERATURE", "0.3")))
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_functions_agent(llm=llm, tools=TOOLS, prompt=prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True,
                         max_iterations=10, handle_parsing_errors=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AI Career Agent starting...")
    yield

app = FastAPI(title="AI Career Agent", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "healthy", "service": "ai-career-agent"}

@app.get("/")
async def root(): return RedirectResponse(url="/docs")

add_routes(app, create_agent(), path="/career-agent",
           enable_feedback_endpoint=True, enable_public_trace_link_endpoint=True)

def _wrap(tool_fn): return RunnableLambda(lambda x: tool_fn.invoke(x.get("input", x)))

add_routes(app, _wrap(resume_analyzer_tool), path="/tools/resume-analyzer")
add_routes(app, _wrap(jd_matcher_tool),      path="/tools/jd-matcher")
add_routes(app, _wrap(interview_prep_tool),   path="/tools/interview-prep")
add_routes(app, _wrap(career_roadmap_tool),   path="/tools/career-roadmap")
add_routes(app, _wrap(cover_letter_tool),     path="/tools/cover-letter")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="0.0.0.0",
                port=int(os.getenv("PORT", "8000")), reload=True)
