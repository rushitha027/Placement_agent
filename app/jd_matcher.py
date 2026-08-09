"""
Job Description Matcher Tool
-----------------------------
Compares a candidate's resume against a job description and produces:
- Match percentage
- Matched and missing keywords
- Tailoring advice to improve alignment
"""

from langchain.tools import tool


@tool
def jd_matcher_tool(input: str) -> str:
    """
    Match a resume against a job description to assess fit and provide tailoring advice.

    Input format (plain text):
        RESUME:
        <paste resume text here>

        JOB_DESCRIPTION:
        <paste full job description here>

    Returns match analysis with keyword overlap, gaps, and specific tailoring recommendations.
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert ATS (Applicant Tracking System) specialist and career advisor. "
                    "You deeply understand how job descriptions are parsed and how resumes are ranked "
                    "against them. You help candidates tailor their resumes to maximize interview chances."
                ),
            ),
            (
                "human",
                (
                    "Analyze the fit between the following resume and job description.\n\n"
                    "{jd_input}\n\n"
                    "Provide your analysis in these sections:\n"
                    "1. 📊 MATCH SCORE — Estimate the resume-to-JD match as a percentage (0–100%) "
                    "with reasoning\n"
                    "2. ✅ MATCHED KEYWORDS — Skills, tools, and requirements already present in resume\n"
                    "3. ❌ MISSING KEYWORDS — Important JD keywords absent from the resume\n"
                    "4. 🎯 ROLE ALIGNMENT — How well the candidate's experience aligns with the role\n"
                    "5. ✏️ TAILORING RECOMMENDATIONS — Specific edits to the resume (what to add, "
                    "rephrase, or highlight) to improve the score\n"
                    "6. 📌 COVER LETTER ANGLE — Key talking points to emphasize in a cover letter "
                    "for this role\n"
                ),
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"jd_input": input})
    return result.content
