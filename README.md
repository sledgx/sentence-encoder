# sentence-encoder

Universal Sentence Encoder Multilingual as a service.

## How to use

All of the following examples will bring you the service on `http://localhost:8080`.

### Basic usage

This will run the service with the default option:

```sh
docker run -d \
    --name sentence-encoder \
    -p 8080:80 \
    sledgx/sentence-encoder
```

### Usage with custom log

You can define the logs verbosity in the `LOG_LEVEL` environment variable:

```sh
docker run -d \
    --name sentence-encoder \
    -e LOG_LEVEL=debug \
    -p 8080:80 \
    sledgx/sentence-encoder
```

Accepted values are `error`, `warning`, `info`, `debug` and `notset`, default is `info`.

## How to make service requests

The service exposes two endpoints with different functionalities.

### Encode

With this method you can convert a text into an embedding vector of size 512.
You can POST the text in json or form data format:

```sh
curl -X POST http://localhost:8080/encode \
    -H 'Content-Type: application/json' \
    -d '{"text":"Hello, World!"}'
```

### Similarity

With this method you can obtain a similarity score between two texts.
You can POST both texts in json format or form data:

```sh
curl -X POST http://localhost:8080/similarity \
    -H 'Content-Type: application/json' \
    -d '{"left_text":"Hello everybody","right_text":"Ciao a tutti"}'
```

## License

Released under the [MIT License](https://github.com/sledgx/sentence-encoder/blob/master/LICENSE).

Universal Sentence Encoder Multilingual model is owned by Google, please refer to this [link](https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3) to get all licensing information.
