from ppy_common import DataUtil, Console
from pweb_http.common.pweb_http_exception import PWebHTTPException
from pweb_http.connect.pweb_rest_http_data import PwebRestCredentials, HTTPRequestData, PWebRestConst
from pweb_http.connect.pweb_rest_http_dto import PwebRestLoginResponse, PwebRestLoginToken
from pweb_http.connect.sdlize import SDLize
from pweb_http.phttp.phttp_const import RequestType
from pweb_http.phttp.pweb_requests import HTTPResponse, PWebRequests


class PWebRestProcessor:
    ENABLE_PRINT_LOG: bool = False
    http_requester: PWebRequests = PWebRequests()
    _credentials: PwebRestCredentials
    _rest_token: PwebRestLoginToken = None

    def __init__(self, credentials: PwebRestCredentials):
        self._credentials = credentials

    def _prepare_json_request_data(self, request_obj: SDLize, json_dict: dict = None):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        if json_dict:
            return {"data": json_dict}
        return json_dict

    def process_error_response(self, response: HTTPResponse, response_data: dict):
        exception_message = "Something happened wrong!"
        http_code = response.httpCode
        if http_code == 403:
            exception_message = "Access denied"

        exception = PWebHTTPException(exception_message).add_raw_response(response_data)
        errors = DataUtil.get_dict_value(response_data, "errors")
        if isinstance(errors, list):
            for error in errors:
                message = DataUtil.get_dict_value(error, "message")
                if message:
                    exception.add_error(message)
        raise exception

    def log(self, text):
        if self.ENABLE_PRINT_LOG:
            Console.log(text)

    def _get_data(self, response: HTTPResponse, response_obj: SDLize, exception=True):
        response_data = response.data
        self.log(response_data)
        if response.status != PWebRestConst.SUCCESS or not response_data:
            if exception:
                self.process_error_response(response=response, response_data=response_data)
            return None
        if response_obj:
            return response_obj.load_dict(response_data)
        return response_data

    def _set_token(self, token: PwebRestLoginToken):
        if not token or not token.accessToken or not token.refreshToken:
            raise PWebHTTPException("Unable to set token")
        self.rest_token = token

    def _init_auth(self):
        request_data = {
            self._credentials.usernameFieldName: self._credentials.username,
            self._credentials.passwordFieldName: self._credentials.password,
        }
        raw_response = self.http_requester.post(url=self._credentials.loginUrl, json_dict={"data": request_data})
        response = self._get_data(response=raw_response, response_obj=PwebRestLoginResponse())
        self._set_token(token=response.token)

    def _renew_token(self):
        pass

    def _init_config(self, is_open_auth: bool = False):
        if not self._credentials:
            raise PWebHTTPException(message="Please provide credentials.")
        self.http_requester.baseUrl = self._credentials.baseUrl

        if is_open_auth:
            return

        if not self.rest_token or not self.rest_token.accessToken:
            self._init_auth()
        self.http_requester.add_bearer_token(self.rest_token.accessToken)

    def _send_request(self, request_data: HTTPRequestData) -> HTTPResponse:
        response = None
        if request_data.request_type == RequestType.POST:
            response = self.http_requester.post(url=request_data.url, json_dict=request_data.json_dict, data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.PUT:
            response = self.http_requester.put(url=request_data.url, json_dict=request_data.json_dict, data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.PATCH:
            response = self.http_requester.patch(url=request_data.url, json_dict=request_data.json_dict, data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.DELETE:
            response = self.http_requester.delete(url=request_data.url, params=request_data.params)
        else:
            response = self.http_requester.get(url=request_data.url, params=request_data.params)
        request_summary = f"URL: {self.http_requester.baseUrl} \nURL Postfix: {request_data.url} \nparams: {request_data.params} \nJSON Data: {request_data.json_dict}"
        self.log(text=request_summary)
        return response

    def process_rest_request(self, request_data: HTTPRequestData, response_obj: SDLize = None):
        self._init_config(is_open_auth=request_data.is_open_auth)
        response: HTTPResponse = self._send_request(request_data=request_data)
        if response.httpCode == 401:
            self._renew_token()
            response: HTTPResponse = self._send_request(request_data=request_data)
        return self._get_data(response=response, response_obj=response_obj, exception=request_data.exception)

    def get_request(self, url: str, params: dict = None, response_obj: SDLize = None, exception: bool = True, is_open_auth: bool = False):
        return self.process_rest_request(request_data=HTTPRequestData(url=url, params=params, request_type=RequestType.GET, exception=exception, is_open_auth=is_open_auth), response_obj=response_obj)

    def delete_request(self, url: str, params: dict = None, response_obj: SDLize = None, exception: bool = True, is_open_auth: bool = False):
        return self.process_rest_request(request_data=HTTPRequestData(url=url, params=params, request_type=RequestType.DELETE, exception=exception, is_open_auth=is_open_auth), response_obj=response_obj)

    def post_request(self, url: str, request_obj: SDLize = None, json_dict: dict = None, data: dict = None, file: dict = None, response_obj: SDLize = None, exception: bool = True, is_open_auth: bool = False):
        json_dict = self._prepare_json_request_data(request_obj=request_obj, json_dict=json_dict)
        return self.process_rest_request(request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file, request_type=RequestType.POST, exception=exception, is_open_auth=is_open_auth), response_obj=response_obj)

    def put_request(self, url: str, request_obj: SDLize = None, json_dict: dict = None, data: dict = None, file: dict = None, response_obj: SDLize = None, exception: bool = True, is_open_auth: bool = False):
        json_dict = self._prepare_json_request_data(request_obj=request_obj, json_dict=json_dict)
        return self.process_rest_request(request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file, request_type=RequestType.PUT, exception=exception, is_open_auth=is_open_auth), response_obj=response_obj)

    def patch_request(self, url: str, request_obj: SDLize = None, json_dict: dict = None, data: dict = None, file: dict = None, response_obj: SDLize = None, exception: bool = True, is_open_auth: bool = False):
        json_dict = self._prepare_json_request_data(request_obj=request_obj, json_dict=json_dict)
        return self.process_rest_request(request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file, request_type=RequestType.PATCH, exception=exception, is_open_auth=is_open_auth), response_obj=response_obj)


