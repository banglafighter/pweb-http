from dataclasses import dataclass

from pweb_http.connect.pweb_rest_http_data import PWebRestConst
from pweb_http.connect.sdlize import SDLize


@dataclass
class PwebRestLoginToken(SDLize):
    accessToken: str = None
    refreshToken: str = None


@dataclass
class PwebRestLoginResponse(SDLize):
    token: PwebRestLoginToken = None


@dataclass
class PwebRestResponse(SDLize):
    status: str = None
    code: str = None
    message: str = None
    data: object = None

    def get_data(self):
        if self.status == PWebRestConst.SUCCESS:
            return self.data
        return None
