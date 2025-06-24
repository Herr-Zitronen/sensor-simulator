FROM python:3.11-slim

# Install CA certificates
#RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY /requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY simulator.py .

CMD ["python", "simulator.py"]
