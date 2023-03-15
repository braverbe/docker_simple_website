FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
