import os
import traceback
import logging
from waitress import serve
from flask import Flask, request, jsonify
from flask_compress import Compress
from flask_cors import CORS
from libs.processor import SentenceProcessor

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')


def getLogLevel() -> str:
    level = os.environ.get('LOG_LEVEL', 'info')

    if level not in ['error', 'warning', 'info', 'debug', 'notset']:
        level = 'info'

    return level.upper()


def createApp():
    app = Flask(__name__)
    app.logger.setLevel(getLogLevel())
    sp = SentenceProcessor()

    app.logger.info('sentence encoder service')

    @app.route('/encode', methods=['POST'])
    def encodeText():
        try:
            app.logger.info('POST /encode')

            text = getInput('text')

            if not validText(text):
                raise Exception('text is null or empty')

            app.logger.debug(f'input sentence: {text}')
            vector = sp.transform(text)

            app.logger.debug(f'output vector: {vector}')
            return jsonify({
                'vector': vector
            })
        except Exception as e:
            app.logger.error(f'request failed with error: {str(e)}')
            app.logger.debug(f'error stack: {traceback.format_exc()}')
            return jsonify({
                'error': str(e)
            }), 500

    @app.route('/similarity', methods=['POST'])
    def computeSimilarity():
        try:
            app.logger.info('POST /similarity')

            left_text = getInput('left_text')
            right_text = getInput('right_text')

            if not validText(left_text):
                raise Exception('left text is null or empty')

            if not validText(right_text):
                raise Exception('right text is null or empty')

            app.logger.debug(f'input left sentence: {left_text}')
            app.logger.debug(f'input right sentence: {right_text}')
            result = sp.similarity(left_text, right_text)

            app.logger.debug(f'output result: {result} - {type(result)}')
            return jsonify({
                'result': result
            })
        except Exception as e:
            app.logger.error(f'request failed with error: {str(e)}')
            app.logger.debug(f'error stack: {traceback.format_exc()}')
            return jsonify({
                'error': str(e)
            }), 500

    def getInput(key: str) -> str:
        data = request.form if request.form else request.json

        if data is None or key not in data:
            return None

        return data[key]

    def validText(text: str) -> bool:
        return text and text.strip()

    CORS(app)
    Compress().init_app(app)

    return app


if __name__ == '__main__':
    app = createApp()
    serve(app, host='0.0.0.0', port=80)
