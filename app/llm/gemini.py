import google.generativeai as genai

from app.config.settings import settings


class GeminiService:

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.model.generate_content(
            prompt
        )

        return response.text