FROM python:3.9.13-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV APP_JWT_SECRET "sekret"

EXPOSE 8080
CMD ["python3", "main.py"]