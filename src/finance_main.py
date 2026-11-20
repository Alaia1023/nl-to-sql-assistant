import argparse

from src.finance_sql_generator import generate_finance_sql
from src.finance_sql_safety import validate_finance_read_only_sql
from src.finance_query_executor import execute_finance_sql


def run_finance_query(question, strategy="F2"):
    print("\n" + "=" * 65)
    print("FINANCIAL NL-to-SQL ASSISTANT")
    print("=" * 65)

    print("\nQuestion:")
    print(question)

    print(f"\nPrompt strategy: {strategy}")

    print("\nGenerating SQL...")

    sql = generate_finance_sql(
        question,
        strategy=strategy,
    )

    print("\nGenerated SQL:")
    print("-" * 65)
    print(sql)
    print("-" * 65)

    print("\nValidating SQL security...")

    validate_finance_read_only_sql(sql)

    print("SQL validation: PASSED")

    print("\nExecuting query...")

    result = execute_finance_sql(sql)

    print("\nQuery Results:")
    print("=" * 65)

    if not result["rows"]:
        print("No matching records found.")

    else:
        print(" | ".join(result["columns"]))
        print("-" * 65)

        for row in result["rows"]:
            print(" | ".join(str(value) for value in row))

    print("-" * 65)
    print(f"Returned rows: {len(result['rows'])}")
    print(f"Results truncated: {result['truncated']}")

    print("\nQuery completed successfully.")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Financial Services NL-to-SQL Assistant"
    )

    parser.add_argument(
        "--question",
        type=str,
        help="Natural language financial question",
    )

    parser.add_argument(
        "--strategy",
        type=str,
        choices=["F1", "F2"],
        default="F2",
        help="Prompt strategy: F1 or F2",
    )

    args = parser.parse_args()

    question = args.question

    if not question:
        question = input(
            "\nEnter your financial question: "
        ).strip()

    if not question:
        print("Error: Question cannot be empty.")
        return

    try:
        run_finance_query(
            question,
            strategy=args.strategy,
        )

    except ValueError as error:
        print("\nSQL validation error:")
        print(error)

    except Exception as error:
        print("\nQuery execution failed:")
        print(error)


if __name__ == "__main__":
    main()
