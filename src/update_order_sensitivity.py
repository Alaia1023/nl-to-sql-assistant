import json
from pathlib import Path

DATA_FILES = [
    Path("data/dev_questions.json"),
    Path("data/test_questions.json"),
]

ORDER_SENSITIVE_IDS = {
    "DEV-007",
    "DEV-022",
    "TEST-007",
    "TEST-022",
}

for file_path in DATA_FILES:
    if not file_path.exists():
        print(f"Skipped: {file_path} does not exist")
        continue

    with file_path.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    for question in questions:
        question_id = question["id"]
        question["order_sensitive"] = (
            question_id in ORDER_SENSITIVE_IDS
        )

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            questions,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Updated: {file_path}")

    for question in questions:
        print(
            question["id"],
            question["order_sensitive"]
        )
