import argparse
import csv
import json
import time
from pathlib import Path

from src.finance_sql_generator import generate_finance_sql
from src.finance_sql_safety import validate_finance_read_only_sql
from src.finance_query_executor import execute_finance_sql


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "finance_questions.json"
RESULTS_DIR = PROJECT_ROOT / "results"

STRATEGIES = ["F1", "F2"]


def normalize_value(value):
    if isinstance(value, float):
        return round(value, 8)

    return value


def normalize_result(result, preserve_order=False):
    rows = [
        tuple(normalize_value(value) for value in row)
        for row in result["rows"]
    ]

    if not preserve_order:
        rows = sorted(rows, key=lambda row: repr(row))

    return {
        "column_count": len(result["columns"]),
        "rows": rows,
    }


def load_questions(limit=0):
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if limit > 0:
        questions = questions[:limit]

    return questions


def evaluate_one(question_data, strategy):
    question_id = question_data["id"]
    question = question_data["question"]
    gold_sql = question_data["gold_sql"]
    preserve_order = question_data.get("order_sensitive", False)

    result = {
        "id": question_id,
        "question": question,
        "strategy": strategy,
        "generated_sql": "",
        "gold_sql": gold_sql,
        "valid": False,
        "executed": False,
        "correct": False,
        "generation_time": None,
        "error": "",
    }

    start_time = time.perf_counter()

    try:
        generated_sql = generate_finance_sql(
            question,
            strategy=strategy,
        )

        result["generation_time"] = round(
            time.perf_counter() - start_time,
            4,
        )

        result["generated_sql"] = generated_sql

        validate_finance_read_only_sql(generated_sql)
        result["valid"] = True

        generated_result = execute_finance_sql(generated_sql)
        gold_result = execute_finance_sql(gold_sql)

        result["executed"] = True

        generated_normalized = normalize_result(
            generated_result,
            preserve_order=preserve_order,
        )

        gold_normalized = normalize_result(
            gold_result,
            preserve_order=preserve_order,
        )

        result["correct"] = (
            generated_normalized == gold_normalized
        )

    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"

    return result


def save_results(results, strategy):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = RESULTS_DIR / f"finance_{strategy}_results.csv"
    json_path = RESULTS_DIR / f"finance_{strategy}_results.json"
    summary_path = RESULTS_DIR / f"finance_{strategy}_summary.json"

    fieldnames = [
        "id",
        "question",
        "strategy",
        "generated_sql",
        "gold_sql",
        "valid",
        "executed",
        "correct",
        "generation_time",
        "error",
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    total = len(results)

    valid_count = sum(item["valid"] for item in results)
    executed_count = sum(item["executed"] for item in results)
    correct_count = sum(item["correct"] for item in results)

    generation_times = [
        item["generation_time"]
        for item in results
        if item["generation_time"] is not None
    ]

    summary = {
        "strategy": strategy,
        "total_questions": total,
        "valid_sql_count": valid_count,
        "valid_sql_rate": round(valid_count / total, 4) if total else 0,
        "execution_success_count": executed_count,
        "execution_success_rate": round(
            executed_count / total, 4
        ) if total else 0,
        "correct_count": correct_count,
        "exact_execution_accuracy": round(
            correct_count / total, 4
        ) if total else 0,
        "average_generation_time": round(
            sum(generation_times) / len(generation_times), 4
        ) if generation_times else None,
    }

    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Financial NL-to-SQL Benchmark"
    )

    parser.add_argument(
        "--strategy",
        choices=["F1", "F2", "all"],
        default="all",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Number of questions to evaluate; 0 means all.",
    )

    args = parser.parse_args()

    questions = load_questions(args.limit)

    strategies = (
        STRATEGIES
        if args.strategy == "all"
        else [args.strategy]
    )

    print("=" * 65)
    print("FINANCIAL NL-to-SQL BENCHMARK")
    print("=" * 65)
    print("Dataset:", DATASET_PATH.name)
    print("Questions:", len(questions))
    print("Strategies:", ", ".join(strategies))

    all_summaries = []

    for strategy in strategies:
        print("\nEvaluating", strategy)
        print("-" * 65)

        results = []

        for index, question_data in enumerate(questions, start=1):
            print(
                f"[{strategy}] "
                f"Question {index}/{len(questions)}: "
                f"{question_data['id']}"
            )

            result = evaluate_one(question_data, strategy)
            results.append(result)

            print(
                "  Valid:", result["valid"],
                "| Executed:", result["executed"],
                "| Correct:", result["correct"],
            )

            if result["error"]:
                print("  Error:", result["error"])

        summary = save_results(results, strategy)
        all_summaries.append(summary)

        print("\n", strategy, "SUMMARY")
        print(json.dumps(summary, indent=2))

    comparison_path = RESULTS_DIR / "finance_comparison.json"

    with comparison_path.open("w", encoding="utf-8") as file:
        json.dump(
            all_summaries,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 65)
    print("FINANCIAL BENCHMARK COMPARISON")
    print("=" * 65)

    for summary in all_summaries:
        print(
            f"{summary['strategy']}: "
            f"Accuracy={summary['exact_execution_accuracy']:.1%}, "
            f"Valid={summary['valid_sql_rate']:.1%}, "
            f"Execution={summary['execution_success_rate']:.1%}, "
            f"Avg Time={summary['average_generation_time']}s"
        )

    print("\nComparison saved to:", comparison_path)


if __name__ == "__main__":
    main()
