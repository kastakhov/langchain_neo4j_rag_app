FROM python:3.12-bookworm

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY ./src/ /app

RUN find . -type d -name "__pycache__" -exec rm -rf {} \;

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
