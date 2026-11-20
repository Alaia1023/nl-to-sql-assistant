import json
from pathlib import Path

from sqlalchemy import text

from src.database import engine
from src.sql_safety import validate_read_only_sql

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATASET_FILES = [
    DATA_DIR / "dev_questions.json",
    DATA_DIR / "test_questions.json",
]

REQUIRED_FIELDS = {
    "id",
    "question",
    "gold_sql",
    "category",
    "difficulty",
}


def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_questions(questions, connection, all_ids):
    for item in questions:
        missing_fields = REQUIRED_FIELDS - item.keys()

        if missing_fields:
            raise ValueError(
                f"{item.get('id', 'Unknown')}: missing fields {missing_fields}"
            )

        question_id = item["id"]

        if question_id in all_ids:
            raise ValueError(f"Duplicate question ID: {question_id}")

        all_ids.add(question_id)

        sql = item["gold_sql"].strip()

        validate_read_only_sql(sql)

        connection.execute(text(sql)).fetchall()

        print(f"{question_id}: SQL is valid.")


def validate_dataset():
    all_ids = set()
    total_questions = 0

    with engine.connect() as connection:
        for file_path in DATASET_FILES:
            questions = load_dataset(file_path)

            print(f"\nChecking {file_path.name}")
            print("-" * 40)

            validate_questions(questions, connection, all_ids)

            total_questions += len(questions)

    print("\nDataset validation completed successfully!")
    print(f"Total questions: {total_questions}")
    print(f"Unique question IDs: {len(all_ids)}")


if __name__ == "__main__":
    validate_dataset()
