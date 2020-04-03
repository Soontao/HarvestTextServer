from flask import Blueprint, request
from error import ParameterLostError
import tesserocr
from PIL import Image
from flasgger import Swagger

image_api = Blueprint("image_api", __name__)


@image_api.route("/tesseract_ocr", methods=["POST"])
def tesseract_ocr():
    """
    tesseract ocr

    english (better) ocr processing, if you want to use other language, set the 'lang' parameter in query
    ---
    tags:
        - ocr
    parameters:
        -   in: formData
            name: image
            type: file
            required: true
            description: The image to upload.
        -   in: query
            name: lang
            type: string
            description: The language of text in the uploaded image
            default: eng
            enum: [eng, chi_tra, chi_sim]
    consumes:
        -   multipart/form-data
    responses:
        200: 
            description: ocr result
            schema:
                type: object
                properties:
                    code:
                        type: integer
                    text:
                        type: string
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
    tesseract ocr supported languages

    supported languages of tesseract ocr 
    ---
    tags:
        - ocr
    responses:
        200:
            description: a list of supported languages
            schema:
                type: object
                properties: 
                    code:
                        type: integer
                    supported_languages:
                        type: array
                        items:
                            type: string
            examples: 
                supported_languages: {"code":200,"supported_languages":["eng"]}
    """
    return {
        "code": 200,
        "supported_languages": tesserocr.get_languages()[1]
    }
