import json
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_PATH = BASE_DIR / "results" / "dev_results.json"


def main():
    with open(RESULTS_PATH, "r", encoding="utf-8") as file:
        results = json.load(file)

    strategies = ["S0", "S1", "S2"]

    print("=" * 70)
    print("DEVELOPMENT SET ERROR ANALYSIS")
    print("=" * 70)

    for strategy in strategies:
        strategy_results = [
            item for item in results
            if item["strategy"] == strategy
        ]

        category_results = defaultdict(list)

        for item in strategy_results:
            category_results[item["category"]].append(item)

        print(f"\n{'=' * 70}")
        print(f"STRATEGY: {strategy}")
        print(f"{'=' * 70}")

        for category, items in sorted(category_results.items()):
            correct = sum(
                item["execution_accuracy"] for item in items
            )

            total = len(items)
            accuracy = correct / total * 100

            print(
                f"{category}: "
                f"{correct}/{total} correct "
                f"({accuracy:.1f}%)"
            )

        incorrect = [
            item for item in strategy_results
            if not item["execution_accuracy"]
        ]

        print(f"\nIncorrect questions: {len(incorrect)}")

        for item in incorrect:
            print("\n" + "-" * 60)
            print(f"Question ID: {item['question_id']}")
            print(f"Category: {item['category']}")
            print(f"Question: {item['question']}")
            print(f"Valid SQL: {item['valid_sql']}")
            print(f"Execution success: {item['execution_success']}")

            if item["error"]:
                print(f"Error: {item['error']}")

            print("\nGenerated SQL:")
            print(item["generated_sql"])

            print("\nGold SQL:")
            print(item["gold_sql"])


if __name__ == "__main__":
    main()
