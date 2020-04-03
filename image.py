from flask import Blueprint, request, jsonify, make_response, send_file
from error import ParameterLostError
import tesserocr
from PIL import Image
from flasgger import Swagger
from cv2 import cv2
import numpy
import io

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


@image_api.route("/edge_detection", methods=["POST"])
def canny_edge_detection():
    """
    edge detection service
    ---
    tags:
        -   image
    parameters:
        -   in: formData
            name: image
            type: file
            required: true
            description: The image to upload.
    responses:
        200:
            description: the edge detection array
            schema:
                type: object
                properties:
                    code:
                        type: integer
                    edges:
                        type: array
                        items:
                            type: array
                            items: 
                                type: integer
                            minItems: 2
                            maxItems: 2

    """
    if 'image' not in request.files:
        raise ParameterLostError("image")

    img = cv2.imdecode(numpy.fromstring(
        request.files['image'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    edges = cv2.Canny(img, 100, 200)
    indices = numpy.where(edges != [0])
    coordinates = zip(indices[0], indices[1])

    return jsonify({
        "code": 200,
        "edges": list(map(lambda a: [int(a[0]), int(a[1])], list(coordinates)))
    })


@image_api.route("/edge_detection_preview", methods=["POST"])
def canny_edge_detection_preview():
    """
    edge detection preview
    ---
    tags:
        -   image
    parameters:
        -   in: formData
            name: image
            type: file
            required: true
            description: The image to upload.
    responses:
        200:
            description: the edge detection preview image
            content:
                image/png:
                    schema:
                        type: string
                        format: binary
    """
    if 'image' not in request.files:
        raise ParameterLostError("image")

    img = cv2.imdecode(numpy.fromstring(
        request.files['image'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    edges = cv2.Canny(img, 100, 200)

    _, f = cv2.imencode(".png", edges)

    return send_file(io.BytesIO(f.tobytes()), "image/png")
