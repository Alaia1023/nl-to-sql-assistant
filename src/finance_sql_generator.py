import re

from src.llm_client import ask_model
from src.finance_prompt_strategies import build_finance_prompt


def generate_finance_sql(question, strategy="F2"):
    prompt = build_finance_prompt(question, strategy)

    response = ask_model(prompt)

    if not isinstance(response, str):
        raise TypeError(
            "The LLM response must be a string."
        )

    sql = response.strip()

    sql = re.sub(
        r"^```(?:sql)?\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()


if __name__ == "__main__":
    question = "Which funds have the highest NAV?"

    sql = generate_finance_sql(
        question,
        strategy="F2"
    )

    print("Question:", question)
    print("\nGenerated SQL:")
    print(sql)
