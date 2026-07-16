import json
import time

from google import genai
from google.genai.errors import ServerError

from app.config.settings import settings
from app.prompts.seo_prompt import build_seo_prompt


class SEOService:
    def __init__(self):

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        self.models = settings.GEMINI_FALLBACK_MODELS

    def clean_json(self, text: str):

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()

    def generate(self, metadata: dict):

        prompt = build_seo_prompt(metadata)

        last_error = None

        for model in self.models:
            print("\n" + "=" * 60)
            print(f"Trying Gemini Model : {model}")
            print("=" * 60)

            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )

                    text = self.clean_json(response.text)

                    print("Gemini Success")

                    return json.loads(text)

                except ServerError as e:
                    last_error = e

                    wait = 2**attempt

                    print(f"{model} busy (Attempt {attempt + 1}/3)")

                    print(f"Retrying in {wait} seconds...")

                    time.sleep(wait)

                except json.JSONDecodeError as e:
                    last_error = e

                    print("Gemini returned invalid JSON")

                    break

                except Exception as e:
                    last_error = e

                    print(f"{model} failed")

                    print(e)

                    break

            print(f"Switching to next model...\n")

        raise Exception(
            "All Gemini models are currently unavailable.\n"
            "Please try again in a few minutes.\n\n"
            f"Last Error:\n{last_error}"
        )
