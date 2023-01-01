import os
import traceback
import logging
from waitress import serve
from flask import Flask, request, jsonify
from flask_compress import Compress
from flask_cors import CORS
from libs.processor import SentenceProcessor

logging.basicConfig(format='%(asctime)s - %(levelname)s :: %(message)s')


def createApp():
    log_level = os.environ.get('LOG_LEVEL', 'info').upper()

    app = Flask(__name__)
    app.logger.setLevel(log_level)
    sp = SentenceProcessor()

    app.logger.info('sentence encoder service')

    @app.route('/encode', methods=['POST'])
    def encodeText():
        try:
            app.logger.info('POST /encode')

            data = request.form if request.form else request.json
            text = data['text']

            if not (text and text.strip()):
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

    CORS(app)
    Compress().init_app(app)

    return app


if __name__ == '__main__':
    app = createApp()
    serve(app, host='0.0.0.0', port=80)
