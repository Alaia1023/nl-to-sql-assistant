from src.sql_generator import generate_sql
from src.query_executor import execute_sql


def run_assistant(question):
    print("\nGenerating SQL...")
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    print("\nValidating and executing SQL...")

    result = execute_sql(sql)

    print("\nQuery Results:")
    print("-" * 60)

    print(" | ".join(result["columns"]))
    print("-" * 60)

    for row in result["rows"]:
        print(" | ".join(str(value) for value in row))

    if result["truncated"]:
        print("\nOnly the first 100 rows are displayed.")

    print(f"\nReturned {len(result['rows'])} rows.")


def main():
    print("=" * 60)
    print("Natural Language to SQL Assistant")
    print("=" * 60)

    while True:
        question = input("\nEnter your question (or type 'exit'): ").strip()

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
