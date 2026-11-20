import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_PATH = PROJECT_ROOT / "data" / "finance_business_knowledge.json"


def load_finance_business_knowledge():
    with KNOWLEDGE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_finance_business_knowledge():
    knowledge = load_finance_business_knowledge()

    sections = [
        f"DOMAIN: {knowledge['domain']}",
        f"DESCRIPTION: {knowledge['description']}",
        "\nCURRENCY POLICY:"
    ]

    for key, value in knowledge["currency_policy"].items():
        sections.append(f"- {key}: {value}")

    sections.append("\nBUSINESS DEFINITIONS:")

    for term, details in knowledge["definitions"].items():
        sections.append(f"\n{term}:")
        for key, value in details.items():
            sections.append(f"- {key}: {value}")

    sections.append("\nBUSINESS RULES:")

    for rule in knowledge["business_rules"]:
        sections.append(f"- {rule}")

    sections.append("\nTABLE RELATIONSHIPS:")

    for relationship in knowledge["relationships"]:
        sections.append(
            f"- {relationship['from']} -> {relationship['to']}: "
            f"{relationship['key']} "
            f"({relationship['cardinality']})"
        )

    return "\n".join(sections)


if __name__ == "__main__":
    print(format_finance_business_knowledge())
