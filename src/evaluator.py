import json

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """You are an expert resume coach and career consultant with deep knowledge of hiring practices, \
ATS (Applicant Tracking Systems), and what makes candidates stand out to recruiters and hiring managers. \
Your job is to evaluate resumes and provide specific, actionable recommendations.

When evaluating a resume, be honest and constructive. Point to exact text that could be improved and explain why. \
Avoid generic advice — every recommendation should be specific to this resume.

Structure your evaluation with exactly these sections:
1. Overall Score (out of 10) with a 2-3 sentence summary
2. Summary / Objective — clarity, relevance, hook, whether it adds value
3. Experience — bullet quality, quantified achievements, action verbs, impact statements, reverse-chronological order
4. Education — relevance, formatting, whether it's appropriately prominent or de-emphasized
5. Skills — relevance, coverage, ATS keyword alignment, notable gaps
6. Formatting & ATS Compatibility — layout clarity, length, section labels, parse-friendliness, font/structure concerns
7. Quick Wins — the top 3 changes to make immediately for the biggest impact

Return your response as a single JSON object with exactly this structure:
{
  "scores": {
    "summary": <int 1-10>,
    "experience": <int 1-10>,
    "education": <int 1-10>,
    "skills": <int 1-10>,
    "formatting": <int 1-10>,
    "overall": <int 1-10>
  },
  "evaluation": "<full markdown evaluation text as a single escaped string>"
}

The "evaluation" field must contain the complete 7-section evaluation exactly as you would normally write it. Do not abbreviate. Return only the JSON object — no additional text before or after it.
"""


def _parse_response(raw: str) -> dict:
    """Parse Claude's JSON response. Falls back gracefully on failure."""
    try:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {"scores": {}, "evaluation": raw}


def evaluate(resume_text: str, role: str = "") -> dict:
    """Send the resume text to Claude and return the evaluation dict."""
    client = Anthropic()

    content = f"Please evaluate the following resume:\n\n{resume_text}"
    if role:
        content = f"The candidate is targeting the role: {role}\n\n" + content

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )

    return _parse_response(message.content[0].text)
