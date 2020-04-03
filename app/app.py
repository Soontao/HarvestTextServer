from flask import Flask, request, jsonify
from flasgger import Swagger
from error import BaseError
from nlp import nlp_api
from image import image_api
from common import common_api

app = Flask(__name__)

app.config['SWAGGER'] = {
    "title": "ML Service",
    "description": "Out-of-Box machine learning web services",
    "version": "0.0.1-alpha",
    "termsOfService": "",
    "uiversion": 3
}

swagger = Swagger(app)

app.register_blueprint(common_api, url_prefix="/")
app.register_blueprint(nlp_api, url_prefix="/api/v1/nlp")
app.register_blueprint(image_api, url_prefix="/api/v1/image")


@app.errorhandler(BaseError)
def handle_invalid_usage(e):
    """
    handle invalid message
    """
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


if __name__ == "__main__":
    app.run()
