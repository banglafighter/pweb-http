from dataclasses import dataclass
from bpy_obj.sdlize import SDLize
from pweb_http.connect.pweb_rest_http_data import PWebRestConst


@dataclass
class PwebRestLoginToken(SDLize):
    accessToken: str = None
    refreshToken: str = None


@dataclass
class PwebRestLoginResponse(SDLize):
    token: PwebRestLoginToken = None


@dataclass
class PwebRestPaginationResponse(SDLize):
    page: int = None
    itemPerPage: int = None
    total: int = None
    totalPage: int = None


@dataclass
class PwebRestResponse(SDLize):
    status: str = None
    code: str = None
    message: str = None
    data: object = None
    pagination: PwebRestPaginationResponse = None

    def get_data(self):
        if self.status == PWebRestConst.SUCCESS:
            return self.data
        return None

    def is_success(self):
        return self.status == PWebRestConst.SUCCESS
