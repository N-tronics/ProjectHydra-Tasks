FROM python:3
WORKDIR /server
COPY server.py .
RUN pip install flask
ENTRYPOINT ["python3", "server.py"]
