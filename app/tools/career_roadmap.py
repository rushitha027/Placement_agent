"""
Career Roadmap Generator Tool
------------------------------
Creates a personalised, step-by-step career roadmap for a candidate covering:
- Short-term goals (0–3 months)
- Mid-term goals (3–12 months)
- Long-term goals (1–3 years)
- Skills to acquire, certifications, projects, and networking tips
"""

from langchain.tools import tool


@tool
def career_roadmap_tool(input: str) -> str:
    """
    Generate a personalised career roadmap to reach a target job role.

    Input format (plain text):
        CURRENT_ROLE: <current position or 'fresher'>
        TARGET_ROLE: <desired job title, e.g. 'Data Engineer'>
        CURRENT_SKILLS: <comma-separated list of skills you already have>
        EDUCATION: <highest qualification>
        TIMELINE: <how soon you want to achieve the target, e.g. '6 months'>

    Returns a structured, time-bound career roadmap with actionable milestones.
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a world-class career strategist and mentor who has helped thousands of "
                    "professionals transition into and advance within the tech industry. You create "
                    "realistic, motivating, and highly actionable career roadmaps tailored to each "
                    "individual's background and goals."
                ),
            ),
            (
                "human",
                (
                    "Create a detailed career roadmap for the following profile:\n\n"
                    "{roadmap_input}\n\n"
                    "Structure the roadmap as follows:\n\n"
                    "## 🎯 GOAL ANALYSIS\n"
                    "- Gap assessment between current state and target role\n"
                    "- Realistic timeline evaluation\n\n"
                    "## 📅 PHASE 1: FOUNDATION (Months 1–3)\n"
                    "- Core skills to learn (with free/paid resources)\n"
                    "- Projects to build\n"
                    "- Certifications to pursue\n\n"
                    "## 📅 PHASE 2: GROWTH (Months 3–9)\n"
                    "- Intermediate skills and advanced topics\n"
                    "- Portfolio projects\n"
                    "- Community involvement (open source, meetups, LinkedIn)\n\n"
                    "## 📅 PHASE 3: JOB READY (Months 9–12+)\n"
                    "- Job search strategy\n"
                    "- Networking approach\n"
                    "- Application and interview preparation\n\n"
                    "## 📚 LEARNING RESOURCES\n"
                    "- Top 5 courses/books/platforms for this role\n\n"
                    "## 🏆 SUCCESS MILESTONES\n"
                    "- Key checkpoints to know you're on track\n\n"
                    "## ⚠️ COMMON PITFALLS TO AVOID\n"
                ),
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"roadmap_input": input})
    return result.content
