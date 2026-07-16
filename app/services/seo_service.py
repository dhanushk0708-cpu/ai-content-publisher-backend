import json

from google import genai

from app.config.settings import settings
from app.prompts.seo_prompt import build_seo_prompt


class SEOService:
    def __init__(self):

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(self, metadata: dict):

        prompt = build_seo_prompt(metadata)

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL, contents=prompt
        )

        text = response.text.strip()

        print("=" * 50)
        print("Gemini Response:")
        print(text)
        print("=" * 50)

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError:
            raise ValueError(f"Gemini returned invalid JSON:\n\n{text}")
