from enum import Enum


class PHTTPConst:
    APPLICATION_JSON = "application/json"
    SUCCESS = "success"
    ERROR = "error"
    UTF8_ENCODING = "utf-8"


class RequestType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
