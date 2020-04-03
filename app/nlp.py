from flask import Blueprint, request
from jiagu import sentiment
from textblob import TextBlob
from langid import classify
from error import ParameterLostError

nlp_api = Blueprint("npl_api", __name__)


@nlp_api.route("/lang_detect")
def lang_detect():
    # pylint: disable=line-too-long
    """
    text language detection
    ---
    tags:
        -   nlp
    parameters:
        -   in: query
            name: text
            type: string
            required: true
            default: hello world!
            description: text content
    responses:
        200:
            description: text detection result
            schema:
                type: object
                properties:
                    code:
                        type: integer
                    lang:
                        type: string
                        enum: [af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu]
                    probability:
                        type: number


    """
    text = request.args.get("text")
    if text is None:
        raise ParameterLostError("text")
    r = classify(text)
    return {
        "code": 200,
        "lang": r[0],
        "probability": r[1]
    }


@nlp_api.route("/sentiment_zh")
def text_sentiment_zh():
    """
    text sentiment for chinese
    ---
    tags:
        - nlp
    parameters:
        -   in: query
            name: text
            type: string
            required: true
            default: 你真棒！
            description: text content
    responses:
        200:
            description: chinese sentiment response
            schema:
                type: object
                properties:
                    code:
                        type: integer
                        description: status code
                    sentiment:
                        type: string
                        enum: [negative, positive]
                    probability:
                        type: integer

    """
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
    """
    text sentiment for english
    ---
    tags:
        - nlp
    parameters:
        -   in: query
            name: text
            type: string
            required: true
            default: How nice you are!
            description: text content
    responses:
        200:
            description: english sentiment response
            schema:
                type: object
                properties:
                    code:
                        type: integer
                        description: status code
                    polarity:
                        type: integer
                        description: >
                            polarity is a float within the range [-1.0, 1.0],
                            value < 0 means negative, > 0 means positive
                        minimum: -1.0
                        maximum: 1.0
                    subjectivity:
                        type: integer
                        minimum: 0.0
                        maximum: 1.0
                        description: >
                            subjectivity is a float within the range [0.0, 1.0]
                            where 0.0 is very objective and 1.0 is very subjective.

    """
    text = request.args.get("text")

    if text is None:
        raise ParameterLostError("sentiment_text")

    tb = TextBlob(text)

    return {
        "code": 200,
        "polarity": tb.sentiment.polarity,
        "subjectivity": tb.sentiment.subjectivity
    }
