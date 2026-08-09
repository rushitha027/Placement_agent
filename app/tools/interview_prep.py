"""
Interview Preparation Tool
---------------------------
Generates role-specific interview questions and model answers covering:
- Technical questions
- Behavioral (STAR method) questions
- HR / cultural fit questions
- Tips for the specific company/role
"""

from langchain.tools import tool


@tool
def interview_prep_tool(input: str) -> str:
    """
    Generate tailored interview questions and model answers for a specific role.

    Input format (plain text):
        ROLE: <job title, e.g. 'Machine Learning Engineer'>
        COMPANY: <company name, optional — e.g. 'Google'>
        EXPERIENCE_LEVEL: <fresher | junior | mid | senior>
        FOCUS_AREAS: <optional — e.g. 'Python, system design, LLMs'>

    Returns a curated set of interview questions with model answers and interview tips.
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a senior technical interviewer and career coach with deep experience "
                    "conducting and preparing candidates for top-tier tech company interviews. "
                    "You create realistic, role-specific interview prep material that truly prepares "
                    "candidates to succeed."
                ),
            ),
            (
                "human",
                (
                    "Generate a comprehensive interview preparation guide based on:\n\n"
                    "{interview_input}\n\n"
                    "Structure your response as follows:\n\n"
                    "## 🔧 TECHNICAL QUESTIONS (5 questions with model answers)\n"
                    "For each: Question → Model Answer → Key Points to Emphasize\n\n"
                    "## 🌟 BEHAVIORAL QUESTIONS — STAR Method (3 questions with model answers)\n"
                    "For each: Question → Situation → Task → Action → Result\n\n"
                    "## 🤝 HR / CULTURAL FIT QUESTIONS (3 questions with tips)\n\n"
                    "## 🧠 TRICKY / UNEXPECTED QUESTIONS (2 questions with approach)\n\n"
                    "## 📝 PRE-INTERVIEW CHECKLIST — Top 10 things to do before the interview\n\n"
                    "## 💬 QUESTIONS TO ASK THE INTERVIEWER — 5 smart questions\n"
                ),
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"interview_input": input})
    return result.content
