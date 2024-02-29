from pweb_http.phttp.pweb_requests import PWebRequests


class ApiDataProcessor:
    pweb_requests = PWebRequests()
    accessToken: str
    refreshToken: str

    def __init__(self):
        self.accessToken = None
        self.refreshToken = None

    def logout(self):
        self.accessToken = None
        self.refreshToken = None

    def login(self, identifier, password):
        pass

    def renew_token(self):
        pass

    def intercept_response(self):
        pass

    def process_api_request(self, url: str, request_type, json_dict: dict = None, form_data: dict = None, params: dict = None, file: dict = None, exception=True, response_obj=None):
        pass

    def get(self, url: str, params: dict = None, exception=True, response_obj=None):
        pass

    def post(self, url: str, json_dict: dict = None, form_data: dict = None, file: dict = None, exception=True, response_obj=None):
        pass

    def delete(self, url: str, params: dict = None, exception=True, response_obj=None):
        pass
