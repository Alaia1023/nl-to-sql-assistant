import argparse
import csv
import json
import time
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)
from collections import Counter
from pathlib import Path

from src.llm_client import ask_model
from src.prompt_strategies import build_prompt
from src.query_executor import execute_sql
from src.sql_safety import validate_read_only_sql


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

STRATEGIES = ["S0", "S1", "S2", "S3"]


def load_questions(split):
    file_path = DATA_DIR / f"{split}_questions.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_result(result, preserve_order=False):
    normalized_rows = []

    for row in result["rows"]:
        normalized_row = []

        for value in row:
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                value = round(float(value), 8)

            normalized_row.append(value)

        normalized_rows.append(
            json.dumps(normalized_row, sort_keys=True, default=str)
        )

    if not preserve_order:
        normalized_rows.sort()

    return {
        "column_count": len(result["columns"]),
        "rows": normalized_rows,
    }

def generate_with_retry(prompt, max_attempts=3):
    retryable_errors = (
        RateLimitError,
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
    )

    for attempt in range(max_attempts):
        try:
            return ask_model(prompt)

        except retryable_errors:
            if attempt == max_attempts - 1:
                raise

            wait_seconds = 2 ** (attempt + 1)
            print(
                f"Temporary API error. "
                f"Retrying in {wait_seconds} seconds..."
            )
            time.sleep(wait_seconds)

def evaluate_one(question_data, strategy):
    question = question_data["question"]
    gold_sql = question_data["gold_sql"]

    result = {
        "question_id": question_data["id"],
        "category": question_data["category"],
        "difficulty": question_data["difficulty"],
        "strategy": strategy,
        "question": question,
        "generated_sql": "",
        "gold_sql": gold_sql,
        "api_success": False,
        "generation_time_seconds": None,
        "valid_sql": False,
        "execution_success": False,
        "execution_accuracy": False,
        "error": "",
    }

    try:
        prompt = build_prompt(question, strategy)

        start_time = time.perf_counter()
        generated_sql = generate_with_retry(prompt)
        generation_time = time.perf_counter() - start_time

        result["generated_sql"] = generated_sql
        result["generation_time_seconds"] = round(generation_time, 4)
        result["api_success"] = True

        validate_read_only_sql(generated_sql)
        result["valid_sql"] = True

        generated_result = execute_sql(generated_sql)
        result["execution_success"] = True

        gold_result = execute_sql(gold_sql)

        preserve_order = question_data.get("order_sensitive", False)

        result["execution_accuracy"] = (
          normalize_result(
            generated_result,
            preserve_order=preserve_order
    )
         == normalize_result(
            gold_result,
            preserve_order=preserve_order
    )
)

    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"

    return result


def calculate_summary(results):
    summary = []

    for strategy in STRATEGIES:
        strategy_results = [
            item for item in results
            if item["strategy"] == strategy
        ]

        total = len(strategy_results)

        if total == 0:
            continue

        valid_count = sum(
            item["valid_sql"] for item in strategy_results
        )

        execution_count = sum(
            item["execution_success"] for item in strategy_results
        )

        correct_count = sum(
            item["execution_accuracy"] for item in strategy_results
        )

        generation_times = [
            item["generation_time_seconds"]
            for item in strategy_results
            if item["generation_time_seconds"] is not None
        ]

        average_time = (
            sum(generation_times) / len(generation_times)
            if generation_times else 0
        )

        summary.append({
            "strategy": strategy,
            "total_questions": total,
            "valid_sql_rate": round(valid_count / total, 4),
            "execution_success_rate": round(execution_count / total, 4),
            "execution_accuracy": round(correct_count / total, 4),
            "average_generation_time_seconds": round(average_time, 4),
        })

    return summary


def save_results(results, summary, split, strategy=None):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if strategy:
        filename_prefix = f"{split}_{strategy}"
    else:
        filename_prefix = split

    csv_path = RESULTS_DIR / f"{filename_prefix}_results.csv"
    json_path = RESULTS_DIR / f"{filename_prefix}_results.json"
    summary_path = RESULTS_DIR / f"{filename_prefix}_summary.json"

    if results:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(results[0].keys())
            )
            writer.writeheader()
            writer.writerows(results)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print(f"\nDetailed results saved to: {csv_path}")
    print(f"Detailed JSON saved to: {json_path}")
    print(f"Summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate NL-to-SQL prompt strategies."
    )

    parser.add_argument(
        "--split",
        choices=["dev", "test"],
        default="dev"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=2
    )

    parser.add_argument(
        "--strategy",
        choices=STRATEGIES,
        default=None,
        help="Evaluate only one prompt strategy."
    )

    args = parser.parse_args()

    questions = load_questions(args.split)

    if args.limit > 0:
        questions = questions[:args.limit]

    strategies_to_run = (
        [args.strategy]
        if args.strategy
        else STRATEGIES
    )

    print("=" * 65)
    print("NL-to-SQL Prompt Strategy Evaluation")
    print("=" * 65)
    print(f"Dataset: {args.split}")
    print(f"Questions: {len(questions)}")
    print(f"Strategies: {', '.join(strategies_to_run)}")

    all_results = []

    for strategy in strategies_to_run:
        print(f"\nEvaluating {strategy}...")

        for index, question_data in enumerate(questions, start=1):
            print(
                f"[{strategy}] "
                f"Question {index}/{len(questions)}: "
                f"{question_data['id']}"
            )

            result = evaluate_one(question_data, strategy)
            all_results.append(result)

            print(
                f"  Valid: {result['valid_sql']} | "
                f"Executed: {result['execution_success']} | "
                f"Correct: {result['execution_accuracy']}"
            )

            if result["error"]:
                print(f"  Error: {result['error']}")

    summary = calculate_summary(all_results)

    print("\n" + "=" * 65)
    print("EVALUATION SUMMARY")
    print("=" * 65)

    for item in summary:
        print(f"\nStrategy: {item['strategy']}")
        print(f"Valid SQL rate: {item['valid_sql_rate']:.2%}")
        print(
            "Execution success rate: "
            f"{item['execution_success_rate']:.2%}"
        )
        print(f"Execution accuracy: {item['execution_accuracy']:.2%}")
        print(
            "Average generation time: "
            f"{item['average_generation_time_seconds']:.4f} seconds"
        )

    save_results(
        all_results,
        summary,
        args.split,
        args.strategy
    )


if __name__ == "__main__":
    main()