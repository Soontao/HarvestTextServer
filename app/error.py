

class BaseError(Exception):
    """
    application base error
    """

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        convert to dict
        """
        return {
            "error_type": self.__class__.__name__,
            "error": self.message,
            "code": self.status_code
        }


class ParameterError(BaseError):
    """
    parameter related error
    """

    status_code = 400


class ParameterLostError(ParameterError):
    """
    parameter lost error
    """

    def __init__(self, param_name):
        ParameterError.__init__(self, f"{param_name} must be provided.")
