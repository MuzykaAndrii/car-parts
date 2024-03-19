from enum import Enum


class HttpHeaders(dict, Enum):
    application_json: dict = {"Content-Type": "application/json"}