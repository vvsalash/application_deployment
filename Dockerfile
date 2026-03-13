FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv supervisor

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY proto /app/proto
COPY utils/save_model.py /app/utils/save_model.py
COPY supervisord.conf /etc/supervisord.conf

RUN uv pip install --system -e .
RUN python /app/utils/save_model.py

EXPOSE 5000 50051

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
