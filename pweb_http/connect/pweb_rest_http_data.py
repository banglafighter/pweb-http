from dataclasses import dataclass
from bpy_obj.sdlize import SDLize
from pweb_http.phttp.phttp_const import RequestType


class PWebRestConst:
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class HTTPRequestData:
    url: str
    request_type: RequestType
    json_dict: dict = None
    data: dict = None
    params: dict = None
    file: dict = None
    exception: bool = True
    is_open_auth: bool = False
    is_data_response: bool = True
    ssl_verify: bool = True


@dataclass
class PwebRestCredentials(SDLize):
    baseUrl: str
    username: str = None
    password: str = None
    usernameFieldName: str = "username"
    passwordFieldName: str = "password"
    loginUrl: str = None
    renewTokenUrl: str = None
