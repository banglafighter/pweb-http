from dataclasses import dataclass

from pweb_http.connect.sdlize import SDLize


@dataclass
class PwebRestLoginToken(SDLize):
    accessToken: str = None
    refreshToken: str = None


@dataclass
class PwebRestLoginResponse(SDLize):
    token: PwebRestLoginToken = None
