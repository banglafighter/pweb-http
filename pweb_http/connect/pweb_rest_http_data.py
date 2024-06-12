from dataclasses import dataclass

from pweb_http.connect.sdlize import SDLize
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


@dataclass
class PwebRestCredentials(SDLize):
    baseUrl: str
    username: str
    password: str
    usernameFieldName: str = "username"
    passwordFieldName: str = "password"
    loginUrl: str = "api/v1/auth/login"
    renewTokenUrl: str = "api/v1/auth/renew-token"
