import os
from dotenv import load_dotenv

load_dotenv()
PROVIDER = os.getenv("AI_PROVIDER", "gemini")


def ask_ai(prompt: str) -> str:
    if PROVIDER == "gemini":
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        r = client.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
        return r.text

    if PROVIDER == "claude":
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return r.content[0].text

    raise ValueError("Unknown AI_PROVIDER: " + str(PROVIDER))
