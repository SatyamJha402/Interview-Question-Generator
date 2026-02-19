from groq import Groq
import json, os, re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json(text: str):
    text = re.sub(r"```json|```", "", text).strip()
    return text

def generate_interview_questions(job_description: str):
    try:
        prompt = f"""
You are a senior hiring manager and technical interviewer.

Generate a COMPLETE interview kit based on the job description.

Job Description:
{job_description}

INSTRUCTIONS
For Technical Questions:
- Generate role-specific and seniority-appropriate content.
- Intern/Junior → Fundamentals, basic concepts, simple problem-solving.
- Mid → applied knowledge, debugging, tradeoffs.
- Senior → scalability, system design, architecture, decision-making.
- Ask about their personal project or previous experience
- Produce 3–7 questions per category.
- Avoid generic or trivia questions.
- Questions must be realistic and used in real interviews. Also ensure they are open-ended where appropriate.
- Avoid trivia based or generic questions.

For Behavioral Questions:
Generate behavioral questions that are aligned with role expectations and assess:
- Communication
- Ownership and accountability
- Team collaboration
- Conflict resolution

EVALUATION RUBRIC RULES
It should cover:
- Technical proficiency
- Problem-solving approach
- Depth of understanding
- Communication skills
- Ask about their personal project or previous experience
Define clear indicators for strong, average and weak responses for each criterion, but keep it shot.
Rubrics MUST directly align with generated questions.
Keep total weights to 100, distributed based on importance of each criterion for the role.

CUSTOM SKILL FOCUS
If a specific skill or area is mentioned (for example: APIs, System Design, Leadership, ML, Databases, Testing, Security),
prioritize that area but DO NOT limit all questions to it.

The interview kit must still cover the full role.
Aim for roughly:
• 30–50% questions related to the focus area
• Remaining questions covering other core skills of the role

If no focus is provided, distribute questions across the role’s typical skill areas.


RETURN ONLY VALID JSON IN THIS EXACT SCHEMA:

{{
    "technical_questions": [
    "string"
    ],
    "behavioral_questions": [
    "string"
    ],
    "evaluation_rubric": [
    {{
        "criteria": "string",
        "weight": number,
        "what_to_look_for": "string"
    }}
    ]
}}

STRICT OUTPUT RULES:
- Output JSON only.
- No markdown.
- No explanation.
- No extra text before or after JSON.
"""


        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.choices[0].message.content
        clean = extract_json(raw)
        parsed = json.loads(clean)

        if (
            "technical_questions" not in parsed or
            "behavioral_questions" not in parsed or
            "evaluation_rubric" not in parsed
        ):
            raise ValueError("Missing required keys")

        return parsed

    except json.JSONDecodeError:
        return {"error": "LLM returned invalid JSON"}

    except Exception as e:
        return {"error": f"LLM request failed: {str(e)}"}