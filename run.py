from app.llm.gemini import ask_gemini
from app.logging.logger import app_logger

def main():

    app_logger.info("Application started")

    question = "Explain Retrieval-Augmented Generation in simple terms."

    answer = ask_gemini(question)

    print("\n")

    print(answer)

    app_logger.info("Application finished successfully")


if __name__ == "__main__":
    main()