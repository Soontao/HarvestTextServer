from flask import Blueprint, request
from jiagu import sentiment
from error import ParameterLostError
from textblob import TextBlob
from langid import classify

nlp_api = Blueprint("npl_api", __name__)


@nlp_api.route("/lang_detect")
def lang_detect():
    text = request.args.get("text")
    if text is None:
        raise ParameterLostError("text")
    r = classify(text)
    return {
        "lang": r[0],
        "probability": r[1]
    }


@nlp_api.route("/sentiment_zh")
def text_sentiment_zh():
    text = request.args.get("text")

    if text is None:
        raise ParameterLostError("sentiment_text")

    result = sentiment(text)

    return {
        "code": 200,
        "sentiment": result[0],
        "probability": result[1]
    }


@nlp_api.route("/sentiment_en")
def text_sentiment_en():
    text = request.args.get("text")

    if text is None:
        raise ParameterLostError("sentiment_text")

    tb = TextBlob(text)

    return {
        "code": 200,
        "polarity": tb.sentiment.polarity,
        "subjectivity": tb.sentiment.subjectivity
    }
