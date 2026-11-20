import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
MODEL_NAME = os.getenv("LLM_MODEL")


PROVIDER_CONFIG = {
    "groq": {
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
    },
    "openrouter": {
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
    },
}


def get_client():
    if PROVIDER not in PROVIDER_CONFIG:
        raise ValueError(
            "LLM_PROVIDER must be 'groq' or 'openrouter'."
        )

    config = PROVIDER_CONFIG[PROVIDER]
    api_key = os.getenv(config["api_key_env"])

    if not api_key:
        raise ValueError(
            f"{config['api_key_env']} is missing from .env"
        )

    if not MODEL_NAME:
        raise ValueError("LLM_MODEL is missing from .env")

    return OpenAI(
        api_key=api_key,
        base_url=config["base_url"],
    )


def ask_model(prompt):
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert SQL assistant. "
                    "Return only one SQLite SELECT query. "
                    "Do not include explanations or Markdown."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
