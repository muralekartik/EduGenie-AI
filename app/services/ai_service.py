import json
import re

from app.config import settings
from app.services import fallback_service
from app.services.gemini_service import GeminiService


class AIService:
    def __init__(self):
        self.gemini = GeminiService()

    async def _generate(self, prompt: str):
        if settings.demo_mode or not settings.gemini_api_key:
            return None

        try:
            result = await self.gemini.generate(prompt)

            if result:
                return result

            return None

        except Exception as error:
            print(f"Gemini error: {error}")
            return None

    async def answer_question(self, question: str, context: str = ""):
        prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.

Question:
{question}

Additional context:
{context or "None"}

Give a student-friendly answer with:
1. Direct answer
2. Simple explanation
3. Example if useful
"""

        result = await self._generate(prompt)

        if result:
            return {
                "answer": result,
                "source": "Google Gemini",
            }

        return fallback_service.answer_question(question, context)

    async def explain_topic(self, topic: str, level: str = "beginner"):
        prompt = f"""
You are EduGenie, an educational AI tutor.

Explain the following topic for a {level}-level student:

Topic:
{topic}

Include:
- Simple definition
- Main concepts
- Easy example
- Key points
"""

        result = await self._generate(prompt)

        if result:
            return {
                "topic": topic,
                "level": level,
                "explanation": result,
                "source": "Google Gemini",
            }

        return fallback_service.explain_topic(topic, level)

    async def summarize_text(self, text: str, length: str = "medium"):
        prompt = f"""
You are EduGenie, an educational AI assistant.

Summarize the following text.

Desired summary length:
{length}

Text:
{text}

Keep the important information and use simple language.
"""

        result = await self._generate(prompt)

        if result:
            return {
                "summary": result,
                "length": length,
                "source": "Google Gemini",
            }

        return fallback_service.summarize_text(text, length)

    async def generate_quiz(self, topic: str, difficulty: str = "medium"):
        prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions about:

{topic}

Difficulty:
{difficulty}

Return ONLY valid JSON in this exact format:

{{
    "quiz": [
        {{
            "question": "Question text",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:
- Exactly 3 questions
- Exactly 4 options per question
- The answer must exactly match one option
- No markdown
"""

        result = await self._generate(prompt)

        if result:
            try:
                data = self._clean_json(result)

                if self._valid_quiz(data):
                    return {
                        "topic": topic,
                        "difficulty": difficulty,
                        "quiz": data["quiz"],
                        "source": "Google Gemini",
                    }

            except Exception as error:
                print(f"Quiz JSON error: {error}")

        return fallback_service.generate_quiz(topic, difficulty)

    async def get_recommendations(self, topic: str = ""):
        prompt = f"""
You are EduGenie, an adaptive learning assistant.

Create 3 useful learning recommendations for a student studying:

{topic or "their current subject"}

For each recommendation provide:
- title
- description
- action

Return ONLY valid JSON:

{{
    "recommendations": [
        {{
            "title": "string",
            "description": "string",
            "action": "string"
        }}
    ]
}}
"""

        result = await self._generate(prompt)

        if result:
            try:
                data = self._clean_json(result)

                if (
                    isinstance(data, dict)
                    and isinstance(data.get("recommendations"), list)
                ):
                    return {
                        "topic": topic,
                        "recommendations": data["recommendations"][:3],
                        "source": "Google Gemini",
                    }

            except Exception as error:
                print(f"Recommendation JSON error: {error}")

        return fallback_service.get_recommendations(topic)

    @staticmethod
    def _clean_json(text: str):
        text = text.strip()

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        return json.loads(text)

    @staticmethod
    def _valid_quiz(data):
        if not isinstance(data, dict):
            return False

        quiz = data.get("quiz")

        if not isinstance(quiz, list) or len(quiz) != 3:
            return False

        for question in quiz:
            if not isinstance(question, dict):
                return False

            options = question.get("options", [])
            answer = question.get("answer")

            if not isinstance(options, list) or len(options) != 4:
                return False

            if answer not in options:
                return False

        return True