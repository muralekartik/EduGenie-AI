import asyncio

from google import genai
from google.genai import types

from app.config import settings


class GeminiService:
    def __init__(self):
        self.client = None

        if settings.gemini_api_key:
            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    async def generate(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError("Gemini API key is not configured.")

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                    ),
                )

                return response.text or ""

            except Exception as error:
                print(
                    f"Gemini attempt {attempt + 1}/3 failed: {error}"
                )

                if (
                    ("503" in str(error))
                    or ("UNAVAILABLE" in str(error))
                ) and attempt < 2:
                    await asyncio.sleep(2 ** attempt)
                    continue

                raise