from flask import Blueprint, request
from error import ParameterLostError
import tesserocr
from PIL import Image

image_api = Blueprint("image_api", __name__)


@image_api.route("/tesseract_ocr", methods=["POST"])
def tesseract_ocr():
    """
    tesseract ocr

    english (better) ocr processing
    """
    if 'image' not in request.files:
        raise ParameterLostError("image")
    lang = request.args.get("lang", "eng")  # default lang
    img = Image.open(request.files["image"])
    text = tesserocr.image_to_text(img, lang)  # ocr processing
    return {
        "code": 200,
        "text": text
    }


@image_api.route("/ocr_supported_languages")
def tesseract_ocr_supported_languages():
    """
    tesseract ocr 

    supported languages
    """
    return {
        "code": 200,
        "supported_languages": tesserocr.get_languages()[1]
    }
