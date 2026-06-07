# CLAUDE.md - data-validator-app

## What it is
Python job that consumes SQS messages, reads Parquet files from S3, validates data quality and sends reports by email. The entire infrastructure runs locally via LocalStack + Mailpit.

## Stack
- Python 3.12, boto3, pandas 2, pyarrow, python-dotenv
- LocalStack (emulates S3 + SQS), Mailpit (captures emails), Kubernetes (jobs), Terraform (local provisioning)

## Structure
```
app.py             -> Entry point: orchestrates SQS → S3 → validation → email
config/            -> Configuration via env vars (get_settings)
models/
  statistics.py    -> Validation statistics model
validators/
  data_validator.py -> Data quality validation logic over DataFrames
services/
  email_service.py -> Sends report by email (SMTP/Mailpit)
  s3_service.py    -> Downloads Parquet from S3 (LocalStack in dev)
  sqs_service.py   -> Consumes SQS messages
utils/             -> Logger
venv/              -> Python virtual environment (do not version)
requirements.txt   -> boto3, pandas, numpy, pyarrow, python-dotenv
```

## Patterns
- Flow: SQS message → S3 download (Parquet) → DataValidator → Statistics → EmailService
- Services isolated by responsibility in `services/`
- Centralized configuration via `config/` with `get_settings()`
- LocalStack for development/testing without real AWS costs
- Kubernetes Job for production execution
