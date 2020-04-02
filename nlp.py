from flask import Blueprint, request
from jiagu import sentiment
from error import ParameterError

nlp_api = Blueprint("npl_api", __name__)


@nlp_api.route("/sent")
def text_sent():
    text = request.args.get("text")
    if text is None:
        raise ParameterError("sentiment text content is not provided.")
    result = sentiment(text)
    return {"sentiment": result[0], "probability": result[1], "code": 200}
