FROM python:3.13-slim

WORKDIR /app

COPY portChecker.py ./portChecker.py
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "portChecker.py"]
