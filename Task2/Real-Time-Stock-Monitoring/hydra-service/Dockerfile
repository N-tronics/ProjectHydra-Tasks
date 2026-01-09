FROM python:3
WORKDIR /server
COPY server.py .
COPY container_metrics.py .
COPY templates ./templates/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y stress-ng
ENTRYPOINT ["python3", "server.py"]
