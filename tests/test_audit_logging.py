import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import src.audit_logger as audit_logger
import src.main as retail
import src.finance_main as finance


class AuditLoggingTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "audit.jsonl"

        self.path_patcher = patch.object(
            audit_logger,
            "AUDIT_LOG_PATH",
            self.log_path,
        )
        self.path_patcher.start()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def read_records(self):
        with self.log_path.open("r", encoding="utf-8") as file:
            return [json.loads(line) for line in file if line.strip()]

    def run_silently(self, function):
        with redirect_stdout(StringIO()):
            try:
                function()
            except Exception as error:
                return error

        return None

    def test_all_eight_scenarios(self):
        scenarios = [
            ("success", "passed", "success"),
            ("rejected", "rejected", "not_run"),
            ("execution_failed", "passed", "failed"),
            ("generation_failed", "not_run", "not_run"),
        ]

        for domain, module in [
            ("retail", retail),
            ("finance", finance),
        ]:
            generator_name = (
                "generate_sql"
                if domain == "retail"
                else "generate_finance_sql"
            )
            executor_name = (
                "execute_sql"
                if domain == "retail"
                else "execute_finance_sql"
            )
            runner = (
                module.run_assistant
                if domain == "retail"
                else module.run_finance_query
            )

            for scenario, expected_validation, expected_execution in scenarios:
                with self.subTest(domain=domain, scenario=scenario):
                    generated_sql = "SELECT 1 AS value"
                    generator_error = None
                    executor_error = None

                    if scenario == "rejected":
                        generated_sql = (
                            "DELETE FROM customers"
                            if domain == "retail"
                            else "DELETE FROM funds"
                        )

                    elif scenario == "generation_failed":
                        generator_error = RuntimeError(
                            "Simulated model error"
                        )

                    elif scenario == "execution_failed":
                        executor_error = sqlite3.OperationalError(
                            "Simulated database error"
                        )

                    generator_patch = patch.object(
                        module,
                        generator_name,
                        return_value=generated_sql,
                        side_effect=generator_error,
                    )

                    executor_patch = patch.object(
                        module,
                        executor_name,
                        return_value={
                            "columns": ["value"],
                            "rows": [(1,)],
                            "truncated": False,
                        },
                        side_effect=executor_error,
                    )

                    with generator_patch, executor_patch:
                        error = self.run_silently(
                            lambda: runner(
                                f"Test {domain} {scenario}"
                            )
                        )

                    if scenario == "success":
                        self.assertIsNone(error)
                    else:
                        self.assertIsNotNone(error)

                    record = self.read_records()[-1]

                    self.assertEqual(record["domain"], domain)
                    self.assertEqual(
                        record["question"],
                        f"Test {domain} {scenario}",
                    )
                    self.assertEqual(
                        record["strategy"],
                        "S2" if domain == "retail" else "F2",
                    )
                    if scenario == "generation_failed":
                        self.assertIsNone(record["generated_sql"])
                    else:
                        self.assertEqual(
                            record["generated_sql"],
                            generated_sql,
                        )

                    self.assertIsInstance(
                        record["generation_time_ms"],
                        (int, float),
                    )
                    if scenario == "success":
                        self.assertEqual(record["returned_rows"], 1)
                    else:
                        self.assertIsNotNone(record["error"])
                    self.assertEqual(
                        record["validation_status"],
                        expected_validation,
                    )
                    self.assertEqual(
                        record["execution_status"],
                        expected_execution,
                    )
                    self.assertIn("timestamp", record)
                    self.assertIn("generation_time_ms", record)
                    self.assertIn("execution_time_ms", record)

        records = self.read_records()
        self.assertEqual(len(records), 8)

    def test_log_is_valid_json_lines(self):
        audit_logger.write_audit_log(
            domain="finance",
            question="Test JSON serialization",
            strategy="F2",
            validation_status="passed",
            execution_status="success",
            returned_rows=1,
        )

        records = self.read_records()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["domain"], "finance")
        self.assertEqual(records[0]["returned_rows"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
