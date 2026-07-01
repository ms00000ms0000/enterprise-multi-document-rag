import google.generativeai as genai

from app.config.settings import settings
from app.logging.logger import app_logger


class GeminiService:

    DEFAULT_MODEL = "gemini-2.5-flash"

    _initialized = False
    _model = None

    def __init__(self):

        self._initialize()

        self.model = (
            GeminiService._model
        )

    @classmethod
    def _initialize(
        cls,
    ):

        if cls._initialized:

            return

        try:

            app_logger.info(
                "Initializing Gemini model..."
            )

            genai.configure(
                api_key=settings.GEMINI_API_KEY
            )

            cls._model = (
                genai.GenerativeModel(
                    cls.DEFAULT_MODEL
                )
            )

            cls._initialized = True

            app_logger.info(
                f"Gemini model "
                f"'{cls.DEFAULT_MODEL}' "
                f"initialized successfully."
            )

        except Exception:

            app_logger.exception(
                "Failed to initialize Gemini."
            )

            raise

    def generate(
        self,
        prompt,
    ):

        if not prompt:

            raise ValueError(
                "Prompt cannot be empty."
            )

        try:

            response = (
                self.model.generate_content(
                    prompt
                )
            )

            if (
                not hasattr(
                    response,
                    "text",
                )
                or not response.text
            ):

                app_logger.warning(
                    "Gemini returned an empty response."
                )

                return (
                    "No response generated."
                )

            return response.text.strip()

        except Exception:

            app_logger.exception(
                "Gemini generation failed."
            )

            raise RuntimeError(
                "Failed to generate answer from Gemini."
            )

    @classmethod
    def model_name(
        cls,
    ):

        return cls.DEFAULT_MODEL

    @classmethod
    def is_initialized(
        cls,
    ):

        return cls._initialized