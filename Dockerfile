# NOTE: this Dockerfile is intentionally janky — Deviax should rewrite
# it during artifact_generation. Specifically:
#   * python:3.9 is EOL; should pin to 3.12-slim or 3.13-slim
#   * runs as root by default; should drop to non-root user
#   * no HEALTHCHECK
#   * doesn't run alembic upgrade head before serving — fresh DB will
#     return 5xx on the first request
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
