"""
AI Career Agent
---------------
A placement-ready AI Career Agent built with LangChain 1.x using the
OpenAI Functions agent executor pattern.

The agent can:
  • Analyze resumes and give ATS-ready feedback
  • Match resumes against job descriptions
  • Generate personalised interview preparation guides
  • Build step-by-step career roadmaps
  • Write tailored cover letters

Usage (standalone):
    from app.agent import create_career_agent, run_agent

    agent = create_career_agent()
    response = run_agent(agent, "Analyze my resume: ...")
"""

import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.tools import (
    resume_analyzer_tool,
    jd_matcher_tool,
    interview_prep_tool,
    career_roadmap_tool,
    cover_letter_tool,
)

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an elite AI Career Agent designed to help job seekers \
land their dream placements. You have deep expertise in:

- Resume writing and ATS optimisation
- Job description analysis and resume tailoring
- Technical and behavioral interview preparation
- Career planning and skill development roadmaps
- Professional cover letter writing

You have access to the following specialised tools:

1. **resume_analyzer_tool** — Deep-dive resume review with ATS score and actionable tips
2. **jd_matcher_tool** — Resume-vs-JD fit analysis with keyword gap report
3. **interview_prep_tool** — Role-specific question bank with model answers
4. **career_roadmap_tool** — Time-bound, personalised career progression plan
5. **cover_letter_tool** — Tailored, professional cover letter generation

Guidelines:
- Always use the most appropriate tool for the user's request.
- Ask clarifying questions before invoking a tool if key information is missing.
- After using a tool, summarise the key takeaways and offer the next logical step.
- Be encouraging, honest, and data-driven in your advice.
- If the user provides a resume or JD, extract the relevant information and pass it clearly to the tool.

Start each session by greeting the user and asking how you can help with their career goals today."""

# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------

TOOLS = [
    resume_analyzer_tool,
    jd_matcher_tool,
    interview_prep_tool,
    career_roadmap_tool,
    cover_letter_tool,
]


def create_career_agent() -> AgentExecutor:
    """
    Create and return a configured AgentExecutor for the AI Career Agent.

    Requires OPENAI_API_KEY to be set in the environment.
    """
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=float(os.getenv("AGENT_TEMPERATURE", "0.3")),
        streaming=True,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_openai_functions_agent(llm=llm, tools=TOOLS, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        return_intermediate_steps=False,
        max_iterations=10,
        handle_parsing_errors=True,
    )

    return agent_executor


# ---------------------------------------------------------------------------
# Simple stateless invoke helper
# ---------------------------------------------------------------------------

def run_agent(agent_executor: AgentExecutor, user_message: str, chat_history: list | None = None) -> str:
    """
    Run the agent with a single user message.

    Args:
        agent_executor: The AgentExecutor returned by create_career_agent().
        user_message: The user's input string.
        chat_history: Optional list of prior messages for multi-turn context.

    Returns:
        The agent's response as a string.
    """
    inputs = {
        "input": user_message,
        "chat_history": chat_history or [],
    }
    result = agent_executor.invoke(inputs)
    return result.get("output", "")


# ---------------------------------------------------------------------------
# Session-aware chain (for LangServe multi-turn endpoint)
# ---------------------------------------------------------------------------

# In-memory store keyed by session_id
_session_store: dict[str, ChatMessageHistory] = {}


def _get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]


def create_career_agent_with_history() -> RunnableWithMessageHistory:
    """
    Wrap the agent executor with per-session message history for the
    /career-agent/stream and /career-agent/invoke LangServe endpoints.
    """
    agent_executor = create_career_agent()

    return RunnableWithMessageHistory(
        agent_executor,
        _get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
