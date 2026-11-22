import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG_PATH = PROJECT_ROOT / "logs" / "audit.jsonl"


def write_audit_log(
    *,
    domain,
    question,
    strategy,
    generated_sql=None,
    validation_status="not_run",
    execution_status="not_run",
    generation_time_ms=None,
    execution_time_ms=None,
    returned_rows=None,
    error=None,
):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "domain": domain,
        "question": question,
        "strategy": strategy,
        "generated_sql": generated_sql,
        "validation_status": validation_status,
        "execution_status": execution_status,
        "generation_time_ms": generation_time_ms,
        "execution_time_ms": execution_time_ms,
        "returned_rows": returned_rows,
        "error": error,
    }

    AUDIT_LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(event, ensure_ascii=False, default=str) + "\n"
        )

    return event
