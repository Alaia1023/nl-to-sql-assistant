from src.llm_client import ask_model
from src.schema import DATABASE_SCHEMA
from src.prompt_strategies import build_prompt


def generate_sql(question, strategy="S2"):
    prompt = build_prompt(question, strategy)

    sql = ask_model(prompt)
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql
