import json
from pathlib import Path

from src.finance_query_executor import execute_finance_sql


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "finance_questions.json"


def validate_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    assert len(questions) == 15, "Expected exactly 15 questions."

    ids = [question["id"] for question in questions]

    assert len(ids) == len(set(ids)), "Duplicate question IDs found."

    required_fields = {
        "id",
        "question",
        "gold_sql",
        "category",
        "difficulty",
        "order_sensitive",
    }

    for question in questions:
        assert required_fields.issubset(question.keys()), (
            f"Missing fields in {question['id']}"
        )

        assert question["difficulty"] in {
            "easy",
            "medium",
            "hard",
        }

        assert isinstance(question["order_sensitive"], bool)

        execute_finance_sql(question["gold_sql"])

        print(
            f"{question['id']}: Gold SQL executed successfully."
        )

    print("\nFINANCE DATASET VALIDATION")
    print("==========================")
    print("Total questions:", len(questions))
    print("Unique IDs:", len(set(ids)))
    print("All Gold SQL queries executed successfully.")


if __name__ == "__main__":
    validate_dataset()
