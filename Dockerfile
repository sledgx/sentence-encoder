FROM alpine:3.14 AS usem
RUN apk add --no-cache wget tar
WORKDIR /download

ARG USEM_MODEL_FILE="usem-large.tar.gz"
ARG USEM_MODEL_LINK="https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3?tf-hub-format=compressed"

RUN wget -O $USEM_MODEL_FILE $USEM_MODEL_LINK
RUN tar -zxvf $USEM_MODEL_FILE
RUN rm $USEM_MODEL_FILE

FROM tensorflow/tensorflow:2.8.0
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY --from=usem /download /model

EXPOSE 80

ENTRYPOINT ["python", "app.py"]