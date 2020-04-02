# run image
FROM python:3.7-slim

WORKDIR /app

# install dependency
RUN apt update
RUN apt install -y python-dev build-essential tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra libtesseract-dev libleptonica-dev pkg-config
RUN pip install -U uwsgi

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--module", "app:app"]
