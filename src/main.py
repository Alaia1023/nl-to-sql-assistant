import time

from src.audit_logger import write_audit_log
from src.sql_generator import generate_sql
from src.sql_safety import validate_read_only_sql
from src.query_executor import execute_sql


def run_assistant(question, strategy="S2"):
    sql = None
    generation_time_ms = None
    execution_time_ms = None
    validation_status = "not_run"
    execution_status = "not_run"
    returned_rows = None

    try:
        print("\nGenerating SQL...")

        generation_start = time.perf_counter()
        try:
            sql = generate_sql(question, strategy=strategy)
        finally:
            generation_time_ms = (
                time.perf_counter() - generation_start
            ) * 1000

        print("\nGenerated SQL:")
        print(sql)

        print("\nValidating and executing SQL...")

        validate_read_only_sql(sql)
        validation_status = "passed"

        execution_start = time.perf_counter()
        try:
            result = execute_sql(sql)
        finally:
            execution_time_ms = (
                time.perf_counter() - execution_start
            ) * 1000

        execution_status = "success"
        returned_rows = len(result["rows"])

        print("\nQuery Results:")
        print("-" * 60)

        print(" | ".join(result["columns"]))
        print("-" * 60)

        for row in result["rows"]:
            print(" | ".join(str(value) for value in row))

        if result["truncated"]:
            print("\nOnly the first 100 rows are displayed.")

        print(f"\nReturned {returned_rows} rows.")

        write_audit_log(
            domain="retail",
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
            domain="retail",
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
    print("=" * 60)
    print("Natural Language to SQL Assistant")
    print("=" * 60)

    while True:
        question = input(
            "\nEnter your question (or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            run_assistant(question)
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
