import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# NOTE: "llama-3.2-90b-text-preview" and "llama-3.3-70b-versatile" have both
# been retired by Groq (the latter on August 16, 2026). "openai/gpt-oss-120b"
# is Groq's current recommended replacement (see
# https://console.groq.com/docs/models for the live list).
MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")


def get_llm(temperature: float = 0.7):
    """Build (or rebuild) the ChatGroq client. Raises a clear error if the
    API key is missing instead of failing deep inside a LangChain call."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Create a .env file (see .env.example) "
            "and add your key from https://console.groq.com/keys"
        )
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=temperature,
    )


# Module-level instance kept for backward compatibility with the rest of
# the codebase (post_generator.py, preprocess.py import `llm` directly).
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME) if GROQ_API_KEY else None


if __name__ == "__main__":
    test_llm = get_llm()
    response = test_llm.invoke("Two most important ingredients in samosa are ")
    print(response.content)
