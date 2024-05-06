
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install aiohttp click

CMD ["python", "server.py"]