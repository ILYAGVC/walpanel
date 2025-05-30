FROM python:3.9

WORKDIR /walpanel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p /walpanel/app/data
ENV PYTHONPATH="${PYTHONPATH}:/walpanel:/walpanel/app"
COPY . .

EXPOSE 8000

