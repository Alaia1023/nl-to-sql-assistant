import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_PATH = PROJECT_ROOT / "data" / "business_knowledge.json"


def load_business_knowledge():
    with KNOWLEDGE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_business_knowledge():
    knowledge = load_business_knowledge()

    sections = [
        f"Business domain: {knowledge['domain']}",
        f"Description: {knowledge['description']}",
        "",
        "Business terminology:"
    ]

    for term in knowledge["terms"]:
        sections.append(f"- Term: {term['term']}")
        sections.append(f"  Definition: {term['definition']}")

        if "calculation" in term:
            sections.append(f"  Calculation: {term['calculation']}")

        if "condition" in term:
            sections.append(f"  Condition: {term['condition']}")

    sections.extend([
        "",
        "Business rules:"
    ])

    for rule in knowledge["business_rules"]:
        sections.append(f"- {rule}")

    sections.extend([
        "",
        "Business table relationships:"
    ])

    for relationship in knowledge["relationships"]:
        sections.append(
            f"- {relationship['from']} -> "
            f"{relationship['to']} "
            f"({relationship['type']})"
        )

    return "\n".join(sections)
