FROM alpine:3.14 AS usem
RUN apk add --no-cache wget tar
WORKDIR /download

RUN wget -O usem-large.tar.gz "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3?tf-hub-format=compressed"
RUN tar -zxvf usem-large.tar.gz

FROM tensorflow/tensorflow:2.8.0
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY --from=usem /download /model

EXPOSE 80

ENTRYPOINT ["python", "app.py"]