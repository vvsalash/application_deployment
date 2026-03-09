FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv supervisor

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY proto /app/proto
COPY supervisord.conf /etc/supervisord.conf

RUN uv pip install --system -e .

EXPOSE 5000 50051

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
