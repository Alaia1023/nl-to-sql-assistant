import json
from pathlib import Path


RESULTS_FILE = Path("results/day2/dev_results.json")

with RESULTS_FILE.open("r", encoding="utf-8") as file:
    results = json.load(file)

s2_results = {
    item["question_id"]: item
    for item in results
    if item["strategy"] == "S2"
}

s3_results = {
    item["question_id"]: item
    for item in results
    if item["strategy"] == "S3"
}

for question_id, s3 in s3_results.items():
    if s3["execution_accuracy"]:
        continue

    s2 = s2_results[question_id]

    print("\n" + "=" * 80)
    print("Question ID:", question_id)
    print("Question:", s3["question"])

    print("\n--- S2 GENERATED SQL ---")
    print(s2["generated_sql"])
    print("S2 Correct:", s2["execution_accuracy"])

    print("\n--- S3 GENERATED SQL ---")
    print(s3["generated_sql"])
    print("S3 Correct:", s3["execution_accuracy"])

    print("\n--- GOLD SQL ---")
    print(s3["gold_sql"])

    if s3["error"]:
        print("\nS3 Error:", s3["error"])
