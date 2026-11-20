import json
from pathlib import Path

from src.query_executor import execute_sql

RESULTS_FILE = Path("results/dev_results.json")

with RESULTS_FILE.open("r", encoding="utf-8") as file:
    results = json.load(file)

incorrect_results = [
    item
    for item in results
    if item["strategy"] == "S2"
    and not item["execution_accuracy"]
]

for item in incorrect_results:
    print("\n" + "=" * 75)
    print("Question ID:", item["question_id"])
    print("Question:", item["question"])

    for label, sql in [
        ("GENERATED SQL", item["generated_sql"]),
        ("GOLD SQL", item["gold_sql"]),
    ]:
        print("\n---", label, "---")
        print(sql)

        try:
            output = execute_sql(sql)

            print("Columns:", output["columns"])
            print("Number of rows:", len(output["rows"]))
            print("Rows:")

            for row in output["rows"]:
                print(row)

            if output.get("truncated", False):
                print("Warning: Results were truncated.")

        except Exception as error:
            print(
                "Execution error:",
                type(error).__name__,
                str(error)
            )
