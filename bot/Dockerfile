FROM python:3.10.6-slim

RUN mkdir /tg-bot
WORKDIR /tg-bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNDUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]