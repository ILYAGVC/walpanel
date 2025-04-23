FROM python:3.9-slim

WORKDIR /walpanel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p /walpanel/app/data
ENV PYTHONPATH="${PYTHONPATH}:/walpanel:/walpanel/app"
COPY . .

EXPOSE 8000

CMD ["bash", "-c", "\
    cd /walpanel/app && \
    alembic upgrade head && \
    (uvicorn main:app --host 0.0.0.0 --port 8000 --reload &) && \
    python bot/main.py"]
