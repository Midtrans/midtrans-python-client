import requests
import json
import sys
from .error_midtrans import MidtransAPIError
from .error_midtrans import JSONDecodeError

class HttpClient(object):
    """
    Http Client Class that is wrapper to Python's `requests` module
    Used to do API call to Midtrans API urls.
    Capable of doing http :request:
    """
    def __init__(self):
        self.http_client = requests

    def request(self, method, server_key, request_url, parameters=dict(), 
        custom_headers=dict(), proxies=dict()):
        """
        Perform http request to an url (supposedly Midtrans API url)
        :param method: http method
        :param server_key: Midtrans API server_key that will be used as basic auth header
        :param request_url: target http url
        :param parameters: dictionary of Midtrans API JSON body as parameter, will be converted to JSON

        :return: tuple of:
        response_dict: Dictionary from JSON decoded response
        response_object: Response object from `requests`
        """

        # allow string of JSON to be used as parameters
        is_parameters_string = isinstance(parameters, str)
        if is_parameters_string:
            try:
                parameters = json.loads(parameters)
            except Exception as e:
                raise JSONDecodeError('fail to parse `parameters` string as JSON. Use JSON string or Dict as `parameters`. with message: `{0}`'.format(repr(e)))

        payload = json.dumps(parameters) if method != 'get' else parameters
        default_headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'user-agent': 'midtransclient-python/1.4.1'
        }
        headers = default_headers

        # only merge if custom headers exist
        if custom_headers:
            headers = {**default_headers, **custom_headers}

        response_object = self.http_client.request(
            method,
            request_url,
            auth=requests.auth.HTTPBasicAuth(server_key, ''),
            data=payload if method != 'get' else None,
            params=payload if method == 'get' else None,
            headers=headers,
            proxies=proxies,
            allow_redirects=True
        )
        # catch response JSON decode error
        try:
            response_dict = response_object.json()
        except json.decoder.JSONDecodeError as e:
            raise JSONDecodeError('Fail to decode API response as JSON, API response is not JSON: `{0}`. with message: `{1}`'.format(response_object.text,repr(e)))

        # raise API error HTTP status code
        if response_object.status_code >= 400:
            raise MidtransAPIError(
                message='Midtrans API is returning API error. HTTP status code: `{0}`. '
                'API response: `{1}`'.format(response_object.status_code,response_object.text),
                api_response_dict=response_dict,
                http_status_code=response_object.status_code,
                raw_http_client_data=response_object
            )
        # raise core API error status code
        if 'status_code' in response_dict.keys() and int(response_dict['status_code']) >= 400 and int(response_dict['status_code']) != 407:
            raise MidtransAPIError(
                'Midtrans API is returning API error. API status code: `{0}`. '
                'API response: `{1}`'.format(response_dict['status_code'],response_object.text),
                api_response_dict=response_dict,
                http_status_code=response_object.status_code,
                raw_http_client_data=response_object
            )

        return response_dict, response_object
