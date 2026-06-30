import google.generativeai as genai

from app.config.settings import settings
from app.logging.logger import app_logger


class GeminiService:

    def __init__(self):

        try:

            genai.configure(
                api_key=settings.GEMINI_API_KEY
            )

            self.model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            app_logger.info(
                "Gemini initialized successfully."
            )

        except Exception:

            app_logger.exception(
                "Failed to initialize Gemini."
            )

            raise

    def generate(
        self,
        prompt: str,
    ) -> str:

        try:

            response = self.model.generate_content(
                prompt
            )

            if not response.text:

                app_logger.warning(
                    "Gemini returned an empty response."
                )

                return "No response generated."

            return response.text

        except Exception:

            app_logger.exception(
                "Gemini generation failed."
            )

            raise RuntimeError(
                "Failed to generate answer from Gemini."
            )