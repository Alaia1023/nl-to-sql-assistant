import json
from pathlib import Path

old_results_path = Path("results/day2/dev_results.json")
new_results_path = Path("results/dev_S3_results.json")

if not old_results_path.exists():
    raise FileNotFoundError(
        "Missing results/day2/dev_results.json. "
        "Please check that the Day 2 results were backed up."
    )

if not new_results_path.exists():
    raise FileNotFoundError(
        "Missing results/dev_S3_results.json."
    )

with old_results_path.open("r", encoding="utf-8") as file:
    old_results = json.load(file)

with new_results_path.open("r", encoding="utf-8") as file:
    new_results = json.load(file)

old_s2 = {
    item["question_id"]: item
    for item in old_results
    if item["strategy"] == "S2"
}

old_s3 = {
    item["question_id"]: item
    for item in old_results
    if item["strategy"] == "S3"
}

new_s3 = {
    item["question_id"]: item
    for item in new_results
}

print("=" * 80)
print("S2 vs OLD S3 vs NEW S3")
print("=" * 80)

for question_id, new_item in new_s3.items():
    s2 = old_s2[question_id]
    old = old_s3[question_id]

    if new_item["execution_accuracy"]:
        continue

    print("\n" + "=" * 80)
    print("Question:", question_id)
    print("Question text:", new_item["question"])

    print(
        "\nAccuracy:"
        f"\n  Old S2: {s2['execution_accuracy']}"
        f"\n  Old S3: {old['execution_accuracy']}"
        f"\n  New S3: {new_item['execution_accuracy']}"
    )

    print("\n--- NEW S3 SQL ---")
    print(new_item["generated_sql"])

    print("\n--- GOLD SQL ---")
    print(new_item["gold_sql"])

print("\n" + "=" * 80)
print("OVERALL COMPARISON")
print("=" * 80)

for label, results in [
    ("Old S2", old_s2),
    ("Old S3", old_s3),
    ("New S3", new_s3),
]:
    correct = sum(
        item["execution_accuracy"]
        for item in results.values()
    )
    print(f"{label}: {correct}/{len(results)} ({correct / len(results):.0%})")
