"""
Cover Letter Generator Tool
-----------------------------
Generates a professional, personalised cover letter tailored to:
- A specific job description
- The candidate's experience and background
- The company's culture and values
"""

from langchain.tools import tool


@tool
def cover_letter_tool(input: str) -> str:
    """
    Generate a professional, personalised cover letter for a job application.

    Input format (plain text):
        CANDIDATE_NAME: <full name>
        ROLE: <job title you are applying for>
        COMPANY: <company name>
        MY_BACKGROUND: <brief summary of your experience and skills>
        JOB_DESCRIPTION: <paste key requirements from the JD — or full JD>
        TONE: <professional | enthusiastic | creative> (optional, default: professional)

    Returns a ready-to-send cover letter (3–4 paragraphs).
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert cover letter writer who crafts compelling, authentic, and "
                    "highly personalised cover letters that get candidates to the interview stage. "
                    "You avoid generic templates and always tailor the letter to the specific role, "
                    "company, and candidate. Your letters are concise (under 400 words), impactful, "
                    "and follow best practices in professional business writing."
                ),
            ),
            (
                "human",
                (
                    "Write a cover letter based on the following details:\n\n"
                    "{cover_letter_input}\n\n"
                    "The cover letter must:\n"
                    "- Open with a compelling hook that shows genuine interest in the company\n"
                    "- Highlight 2–3 specific, quantified achievements that match the JD requirements\n"
                    "- Demonstrate knowledge of the company's mission/values\n"
                    "- End with a confident, professional call to action\n"
                    "- Be between 300–400 words\n"
                    "- Use a formal letter format with date, salutation, body, and closing\n\n"
                    "After the letter, add a section:\n"
                    "## 💡 CUSTOMIZATION TIPS\n"
                    "List 3 specific things the candidate should personalise further before sending.\n"
                ),
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"cover_letter_input": input})
    return result.content
