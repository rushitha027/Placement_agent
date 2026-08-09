import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.tools import (
    resume_analyzer_tool, jd_matcher_tool, interview_prep_tool,
    career_roadmap_tool, cover_letter_tool,
)

SYSTEM_PROMPT = """You are an elite AI Career Agent helping job seekers land placements.
Tools: resume_analyzer_tool, jd_matcher_tool, interview_prep_tool, career_roadmap_tool, cover_letter_tool.
Always pick the right tool, ask for missing info, and summarise after each response."""

TOOLS = [resume_analyzer_tool, jd_matcher_tool, interview_prep_tool, career_roadmap_tool, cover_letter_tool]
_session_store: dict = {}

def _get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]

def create_career_agent() -> AgentExecutor:
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                     temperature=float(os.getenv("AGENT_TEMPERATURE", "0.3")), streaming=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_functions_agent(llm=llm, tools=TOOLS, prompt=prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=10, handle_parsing_errors=True)

def create_career_agent_with_history() -> RunnableWithMessageHistory:
    return RunnableWithMessageHistory(
        create_career_agent(), _get_session_history,
        input_messages_key="input", history_messages_key="chat_history",
    )
