FROM python:3.10.6-slim

RUN mkdir /django-app
WORKDIR /django-app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNDUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8080

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "my_delivery.wsgi:application"]