FROM python:3
WORKDIR /app
COPY app/* .
RUN pip install flask
EXPOSE 8000
ENTRYPOINT ["python3", "server.py"]
