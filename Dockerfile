FROM python:3.12.3-slim

WORKDIR /app

COPY main.py config.py llmmod.py .chainlit/ prompts.md poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry==1.8.5 \
  && poetry config virtualenvs.in-project true
RUN poetry install


ENV PYTHONUNBUFFERED=on

CMD ["poetry", "run", "chainlit", "run", "main.py", "--port=8080", "--host=0.0.0.0", "--headless", "-d"]
