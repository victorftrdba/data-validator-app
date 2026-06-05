# CLAUDE.md - data-validator-app

## O que é
Job Python que consome mensagens SQS, lê arquivos Parquet do S3, valida qualidade dos dados e envia relatórios por e-mail. Toda a infraestrutura roda localmente via LocalStack + Mailpit.

## Stack
- Python 3.12, boto3, pandas 2, pyarrow, python-dotenv
- LocalStack (emula S3 + SQS), Mailpit (captura e-mails), Kubernetes (jobs), Terraform (provisionamento local)

## Estrutura
```
app.py             -> Entry point: orquestra SQS → S3 → validação → e-mail
config/            -> Configurações via env vars (get_settings)
models/
  statistics.py    -> Modelo de estatísticas de validação
validators/
  data_validator.py -> Lógica de validação de qualidade sobre DataFrames
services/
  email_service.py -> Envio de relatório por e-mail (SMTP/Mailpit)
  s3_service.py    -> Download de Parquet do S3 (LocalStack em dev)
  sqs_service.py   -> Consumo de mensagens SQS
utils/             -> Logger
venv/              -> Ambiente virtual Python (não versionar)
requirements.txt   -> boto3, pandas, numpy, pyarrow, python-dotenv
```

## Padrões
- Fluxo: SQS message → S3 download (Parquet) → DataValidator → Statistics → EmailService
- Serviços isolados por responsabilidade em `services/`
- Configuração centralizada via `config/` com `get_settings()`
- LocalStack para desenvolvimento/testes sem custos AWS reais
- Kubernetes Job para execução em produção
