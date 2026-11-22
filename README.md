# NL-to-SQL Assistant

**An experimental LLM-powered Natural Language-to-SQL system for Retail and Financial Services.**

This project explores how schema-aware prompting, domain-specific business knowledge, and SQL validation can improve natural language database querying.

It includes two independent application domains: an online retail database and a financial portfolio management database. It also provides evaluation workflows for comparing prompt strategies and analyzing generated SQL.

---

## 1. Project Overview

The goal is to allow users to query structured databases using natural language instead of writing SQL manually.

The project focuses on four areas:

- **Accuracy:** Improving SQL generation through schema context, business definitions, and prompt engineering.
- **Business Context:** Incorporating domain-specific terminology, business rules, and table relationships.
- **SQL Safety:** Validating generated queries and restricting database execution to read-only operations.
- **Evaluation:** Comparing prompt strategies using reference SQL queries and execution-based evaluation.

### Supported Domains

| Domain | Description |
|---|---|
| Retail | Customers, orders, products, and order items |
| Finance | Funds, portfolios, securities, positions, transactions, and NAV history |

The financial database is a synthetic portfolio management dataset designed for experimentation.

---

## 2. System Architecture

```text
             Natural Language Question
                       |
                       v
              Prompt Construction
                       |
             +---------+---------+
             |                   |
             v                   v
        Database Schema    Business Knowledge
             |                   |
             +---------+---------+
                       |
                       v
                 LLM Provider
                (Groq / OpenRouter)
                       |
                       v
                 SQL Generation
                       |
                       v
                 SQL Validation
                       |
                       v
              Read-only Execution
                       |
                       v
                 Query Results
                       |
                       v
              Evaluation & Analysis
```

---

## 3. Key Features

### Natural Language-to-SQL Generation

- Converts natural language questions into SQLite queries.
- Uses schema-aware prompts to provide database context.
- Supports separate Retail and Finance workflows.
- Uses OpenAI-compatible APIs through configurable providers.

### Business Knowledge Integration

- Domain-specific terminology and definitions.
- Business rules for interpreting user questions.
- Explicit table relationships and query guidance.
- Financial concepts such as NAV, portfolio exposure, and trading value.

### Prompt Engineering

Retail strategies:
- S0: Schema-based prompting.
- S1: Enhanced schema and join guidance.
- S2: Few-shot prompting.
- S3: Few-shot prompting with business knowledge.

Finance strategies:
- F1: Schema-based prompting.
- F2: Schema and business knowledge integration.

### SQL Safety

- SQL validation using SQLGlot.
- Read-only SQLite database connections.
- SQLite query-only mode.
- Allowed-table restrictions.
- Query execution timeout.
- Maximum result-row limit.

These controls provide safeguards for this experimental application. They are not a substitute for a complete production security architecture.

### SQL Audit Logging

- Shared audit logger for Retail and Finance workflows.
- Structured JSON Lines (`.jsonl`) audit records.
- Records timestamps, domain, user questions, prompt strategies, and generated SQL.
- Tracks SQL validation and execution outcomes.
- Records generation time, execution time, returned row count, and errors.
- Captures successful queries, rejected SQL, execution failures, and generation failures.
- Local audit logs are excluded from Git through `.gitignore`.

Audit logging is currently a local prototype feature. It does not yet provide sensitive-data redaction, centralized log storage, or role-based access controls.

### Evaluation and Analysis

- Development and held-out test question sets for Retail.
- A separate Finance question dataset.
- Execution-based comparison against reference SQL results.
- Valid SQL and execution success measurements.
- Generation-time measurements.
- CSV and JSON result exports.
- Mismatch inspection and regression analysis.
- Manual semantic review for selected evaluation cases.

---

## 4. Project Structure

```text
nl-to-sql-assistant/
│
├── data/
│   ├── shop.db
│   ├── finance.db
│   ├── business_knowledge.json
│   ├── finance_business_knowledge.json
│   ├── dev_questions.json
│   ├── test_questions.json
│   ├── finance_questions.json
│   └── dev_semantic_review.json
│
├── results/
│   ├── day1/
│   ├── day2/
│   ├── dev_results.csv
│   ├── dev_results.json
│   ├── dev_summary.json
│   ├── dev_S3_results.csv
│   ├── dev_S3_results.json
│   ├── dev_S3_summary.json
│   ├── finance_F1_results.csv
│   ├── finance_F1_results.json
│   ├── finance_F1_summary.json
│   ├── finance_F2_results.csv
│   ├── finance_F2_results.json
│   ├── finance_F2_summary.json
│   └── finance_comparison.json
│
├── src/
│   ├── __init__.py
│   ├── audit_logger.py
│   │
│   ├── Retail Application
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   ├── sql_generator.py
│   │   ├── sql_safety.py
│   │   └── query_executor.py
│   │
│   ├── Finance Application
│   │   ├── finance_main.py
│   │   ├── finance_database.py
│   │   ├── finance_models.py
│   │   ├── finance_schema.py
│   │   ├── finance_sql_generator.py
│   │   ├── finance_sql_safety.py
│   │   └── finance_query_executor.py
│   │
│   ├── Business Knowledge & Prompt Engineering
│   │   ├── business_knowledge.py
│   │   ├── finance_business_knowledge.py
│   │   ├── prompt_strategies.py
│   │   └── finance_prompt_strategies.py
│   │
│   ├── LLM Integration
│   │   └── llm_client.py
│   │
│   ├── Evaluation & Analysis
│   │   ├── evaluate.py
│   │   ├── finance_evaluate.py
│   │   ├── analyze_results.py
│   │   ├── compare_s3_runs.py
│   │   ├── inspect_mismatches.py
│   │   ├── inspect_s3_regressions.py
│   │   └── semantic_review.py
│   │
│   └── Data Preparation & Validation
│       ├── create_tables.py
│       ├── seed_data.py
│       ├── seed_finance_data.py
│       ├── query_database.py
│       ├── validate_dataset.py
│       ├── validate_finance_dataset.py
│       └── update_order_sensitivity.py
│
├── tests/
│   └── test_audit_logging.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| SQLite | Relational databases |
| SQLAlchemy | Database models and database interaction |
| SQLGlot | SQL parsing and validation |
| OpenAI Python SDK | LLM API client |
| Groq | Default LLM API provider |
| OpenRouter | Alternative API provider |
| Pandas | Evaluation result processing |
| python-dotenv | Environment configuration |

---

## 6. Installation

### Prerequisites

- Python 3.12 recommended.
- A Groq or OpenRouter API key.
- Git.

### Step 1: Clone the repository

```bash
git clone https://github.com/Alaia1023/nl-to-sql-assistant.git
cd nl-to-sql-assistant
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the LLM provider

Create a local environment file:

```bash
cp .env.example .env
```

Configure the required variables:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-20b
```

For OpenRouter, configure `LLM_PROVIDER=openrouter`, your OpenRouter API key, and a model supported by your account.

**Important:** Never commit `.env` or expose API keys.

---

## 7. Usage

Run all commands from the project root.

### Retail Assistant

Start the interactive assistant:

```bash
python -m src.main
```

Enter a natural language question when prompted. Type `exit` to quit.

Example questions:

- How many orders has each customer placed?
- Which products generated the highest revenue?
- What is the total spending of each customer?

### Finance Assistant

Run the interactive assistant:

```bash
python -m src.finance_main
```

Or provide a question directly:

```bash
python -m src.finance_main --question "Show the total market value of each portfolio on October 31, 2026." --strategy F2
```

Available strategies: `F1`, `F2`.

The default strategy is `F2`.

Example financial questions:

- What is the total market value of each portfolio?
- Calculate the exposure percentage of each sector in a portfolio.
- Show the latest NAV per share for each fund.
- Calculate BUY and SELL trading values during October 2026.

---

## 8. Evaluation and Benchmarking

### Retail Evaluation

Evaluate a small development sample:

```bash
python -m src.evaluate --split dev --limit 5
```

Evaluate a specific strategy:

```bash
python -m src.evaluate --split dev --limit 5 --strategy S3
```

Evaluate the held-out test split:

```bash
python -m src.evaluate --split test --limit 5
```

The `--limit` parameter controls the number of questions. A value of `0` evaluates the full selected split.

Available strategies: `S0`, `S1`, `S2`, `S3`.

### Finance Evaluation

Evaluate a small sample using F2:

```bash
python -m src.finance_evaluate --strategy F2 --limit 3
```

Compare both strategies on a small sample:

```bash
python -m src.finance_evaluate --strategy all --limit 3
```

Evaluate the full Finance dataset:

```bash
python -m src.finance_evaluate --strategy all --limit 0
```

**Note:** Full benchmark runs make multiple LLM API requests and may be affected by provider rate limits or usage quotas.

### Dataset Validation

Validate the Retail datasets:

```bash
python -m src.validate_dataset
```

Validate the Finance dataset and its reference SQL queries:

```bash
python -m src.validate_finance_dataset
```

---

## 9. Evaluation Methodology

The evaluation framework measures several aspects of generated SQL:

| Metric | Meaning |
|---|---|
| Valid SQL Rate | Percentage of generated queries passing SQL validation |
| Execution Success Rate | Percentage of queries that execute successfully |
| Execution Accuracy | Percentage of executed queries matching reference results |
| Average Generation Time | Average time spent generating SQL |

The current exact-result evaluator compares query result structures and values, with row ordering handled according to the dataset's order-sensitivity settings.

This approach is useful for reproducible comparisons but has limitations: semantically equivalent SQL can produce different result structures, and strict comparisons may penalize valid alternative formulations.

For selected disputed cases, a separate semantic review process is used to document manual judgments.

API errors, rate limits, and connection failures should be treated as untested cases rather than incorrect SQL predictions.

Benchmark results are stored under `results/`.

---

## 10. Security Considerations

The prototype implements several SQL execution safeguards:

- SQL parsing and validation with SQLGlot.
- Restrictions on allowed database tables.
- Read-only SQLite connection mode.
- SQLite `query_only` mode.
- Query execution time limits.
- Maximum result-row limits.

These mechanisms reduce the risk of unintended database modifications and uncontrolled queries.

The application also writes structured local audit records to `logs/audit.jsonl`. Records include the domain, question, generated SQL, validation and execution status, timing information, returned row count, and errors. The `logs/` directory is excluded from version control.

Audit logs may contain user questions and generated SQL. Sensitive-data redaction, centralized log management, retention policies, and access controls have not yet been implemented.

However, the project is not production-ready. It does not provide a complete enterprise security model, comprehensive authentication, or deployment-level access control.

The LLM provider is external to the local database. Prompts and relevant schema/business context are sent to the configured provider. Users should not assume that all processing remains on-premises.

The included databases contain synthetic demonstration data.

---

## 11. Current Limitations

- The system depends on external LLM API availability and rate limits.
- SQL generation quality varies across models and prompt strategies.
- Exact-result evaluation cannot fully capture semantic equivalence.
- The current datasets are relatively small and domain-specific.
- The project is a command-line prototype without a production web interface.
- Automated audit logging tests currently cover eight Retail and Finance execution scenarios.

---

## 12. Future Improvements

- Expand semantic SQL evaluation and equivalence checking.
- Expand automated unit and integration test coverage beyond audit logging.
- Expand financial domain knowledge and business rules.
- Add more complex benchmark datasets.
- Build an interactive demonstration interface.
- Explore deployment architectures with stronger data privacy controls.

---

## Author

An independent portfolio project exploring LLM-powered database querying, domain-specific business knowledge, SQL safety, and evaluation-driven prompt engineering.