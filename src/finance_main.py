import argparse
import time

from src.audit_logger import write_audit_log
from src.finance_sql_generator import generate_finance_sql
from src.finance_sql_safety import validate_finance_read_only_sql
from src.finance_query_executor import execute_finance_sql


def run_finance_query(question, strategy="F2"):
    sql = None
    generation_time_ms = None
    execution_time_ms = None
    validation_status = "not_run"
    execution_status = "not_run"
    returned_rows = None

    try:
        print("\n" + "=" * 65)
        print("FINANCIAL NL-to-SQL ASSISTANT")
        print("=" * 65)

        print("\nQuestion:")
        print(question)

        print(f"\nPrompt strategy: {strategy}")
        print("\nGenerating SQL...")

        generation_start = time.perf_counter()
        try:
            sql = generate_finance_sql(
                question,
                strategy=strategy,
            )
        finally:
            generation_time_ms = (
                time.perf_counter() - generation_start
            ) * 1000

        print("\nGenerated SQL:")
        print("-" * 65)
        print(sql)
        print("-" * 65)

        print("\nValidating SQL security...")

        validate_finance_read_only_sql(sql)
        validation_status = "passed"

        print("SQL validation: PASSED")
        print("\nExecuting query...")

        execution_start = time.perf_counter()
        try:
            result = execute_finance_sql(sql)
        finally:
            execution_time_ms = (
                time.perf_counter() - execution_start
            ) * 1000

        execution_status = "success"
        returned_rows = len(result["rows"])

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
        print(f"Returned rows: {returned_rows}")
        print(f"Results truncated: {result['truncated']}")
        print("\nQuery completed successfully.")

        write_audit_log(
            domain="finance",
            question=question,
            strategy=strategy,
            generated_sql=sql,
            validation_status=validation_status,
            execution_status=execution_status,
            generation_time_ms=generation_time_ms,
            execution_time_ms=execution_time_ms,
            returned_rows=returned_rows,
        )

        return result

    except Exception as error:
        if validation_status == "not_run" and sql is not None:
            validation_status = "rejected"

        if validation_status == "passed":
            execution_status = "failed"

        write_audit_log(
            domain="finance",
            question=question,
            strategy=strategy,
            generated_sql=sql,
            validation_status=validation_status,
            execution_status=execution_status,
            generation_time_ms=generation_time_ms,
            execution_time_ms=execution_time_ms,
            returned_rows=returned_rows,
            error=f"{type(error).__name__}: {error}",
        )

        raise


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
