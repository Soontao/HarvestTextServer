from flask import Flask, request, jsonify
from error import BaseError
from nlp import nlp_api
from image import image_api

app = Flask(__name__)


app.register_blueprint(nlp_api, url_prefix="/api/v1/nlp")
app.register_blueprint(image_api, url_prefix="/api/v1/image")


@app.route("/")
def entry_status():
    return {
        "service": "Machine Learning Web Service",
        "code": 200
    }


@app.errorhandler(BaseError)
def handle_invalid_usage(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


if __name__ == "__main__":
    app.run()
