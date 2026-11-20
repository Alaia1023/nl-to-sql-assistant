import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_RESULTS = PROJECT_ROOT / "results" / "dev_S3_results.json"
DEFAULT_REVIEW = PROJECT_ROOT / "data" / "dev_semantic_review.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def display_case(result, review):
    question_id = result["question_id"]

    print("\n" + "=" * 80)
    print(f"Question ID: {question_id}")
    print("=" * 80)

    print("\nQUESTION")
    print(result["question"])

    print("\nSEMANTIC RULE")
    print(review["semantic_rule"])

    print("\nREQUIRED COLUMNS")
    print(", ".join(review["required_columns"]))

    print("\nOPTIONAL COLUMNS")
    optional_columns = review.get("optional_columns", [])
    print(", ".join(optional_columns) if optional_columns else "None")

    print("\nGENERATED SQL")
    print(result["generated_sql"])

    print("\nGOLD SQL")
    print(result["gold_sql"])

    print("\nEXECUTION STATUS")
    print(f"Valid SQL: {result.get('valid_sql')}")
    print(f"Execution success: {result.get('execution_success')}")
    print(f"Exact execution accuracy: {result.get('execution_accuracy')}")

    print("\nREVIEW NOTES")
    print(review.get("notes", "None"))

    print(f"\nREVIEW STATUS: {review.get('review_status', 'pending').upper()}")


def main():
    parser = argparse.ArgumentParser(
        description="Review semantic correctness of NL-to-SQL benchmark results."
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
        help="Path to benchmark results JSON."
    )
    parser.add_argument(
        "--review",
        type=Path,
        default=DEFAULT_REVIEW,
        help="Path to semantic review JSON."
    )
    args = parser.parse_args()

    results = load_json(args.results)
    reviews = load_json(args.review)

    results_by_id = {
        item["question_id"]: item
        for item in results
    }

    print("=" * 80)
    print("NL-to-SQL SEMANTIC REVIEW")
    print("=" * 80)
    print(f"Benchmark results: {args.results}")
    print(f"Review criteria: {args.review}")
    print(f"Cases to review: {len(reviews)}")

    missing_ids = []

    for question_id, review in reviews.items():
        result = results_by_id.get(question_id)

        if result is None:
            missing_ids.append(question_id)
            print(f"\nWARNING: No benchmark result found for {question_id}")
            continue

        display_case(result, review)

    print("\n" + "=" * 80)
    print("REVIEW SUMMARY")
    print("=" * 80)

    for status in ["approved", "rejected", "pending"]:
        count = sum(
            1
            for review in reviews.values()
            if review.get("review_status", "pending") == status
        )
        print(f"{status.capitalize()}: {count}")

    if missing_ids:
        print("Missing benchmark results:", ", ".join(missing_ids))

    print("\nNo semantic accuracy is calculated automatically.")
    print("Each case must be manually reviewed before approval.")


if __name__ == "__main__":
    main()
