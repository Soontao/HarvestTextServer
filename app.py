from flask import Flask, request, jsonify
from error import ParameterError
from nlp import nlp_api

app = Flask(__name__)


app.register_blueprint(nlp_api, url_prefix="/api/v1/nlp")


@app.errorhandler(ParameterError)
def handle_invalid_usage(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


if __name__ == "__main__":
    app.run()
