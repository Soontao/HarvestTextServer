from flask import Blueprint, request

common_api = Blueprint("common_api", __name__)


@common_api.route("/")
def entry_status():
    """
    metric api

    response success when server is up
    ---
    tags:
        - common
    responses:
        200:
            description: server ping-pong response
            schema:
                name: ServerMetircResponse
                type: object
                properties:
                    code:
                        type: integer
                    docs:
                        type: string
                        default: http://127.0.0.1:5000/apidocs
                    service:
                        type: string
    """

    return {
        "service": "Machine Learning Web Service",
        "code": 200,
        "docs": f"{request.url_root}apidocs"
    }
