"""
Resume Analyzer Tool
--------------------
Analyzes a resume text and returns structured feedback covering:
- Key strengths
- Skill gaps for a target role
- ATS (Applicant Tracking System) optimization tips
- Formatting suggestions
"""

from langchain.tools import tool


@tool
def resume_analyzer_tool(input: str) -> str:
    """
    Analyze a resume and provide detailed placement-ready feedback.

    Input format (plain text):
        RESUME:
        <paste resume text here>

        TARGET_ROLE: <optional — e.g. 'Data Scientist' or 'Backend Engineer'>

    Returns structured feedback with strengths, gaps, ATS tips, and formatting advice.
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert career coach and resume reviewer with 15+ years of experience "
                    "in tech recruitment. Your goal is to help candidates land their dream job by "
                    "providing honest, actionable, and detailed resume feedback."
                ),
            ),
            (
                "human",
                (
                    "Please analyze the following resume and provide structured feedback.\n\n"
                    "{resume_input}\n\n"
                    "Return your analysis in the following sections:\n"
                    "1. 📋 SUMMARY — Brief overview of the candidate's profile\n"
                    "2. ✅ STRENGTHS — What is working well (bullet points)\n"
                    "3. ⚠️ GAPS & WEAKNESSES — Missing skills or experience for the target role\n"
                    "4. 🔍 ATS OPTIMIZATION — Keywords to add, formatting fixes for ATS parsers\n"
                    "5. 💡 ACTIONABLE SUGGESTIONS — Top 5 specific improvements\n"
                    "6. 🏆 OVERALL SCORE — Rate the resume out of 10 with a brief justification\n"
                ),
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"resume_input": input})
    return result.content
