import pytest
from unittest.mock import patch
from .helpers import is_str
from .context import HttpClient
import datetime
from pprint import pprint

def test_http_client_class():
    http_client = HttpClient()
    assert type(http_client.http_client).__name__ == 'module'

def test_has_request_method():
    http_client = HttpClient()
    methods = dir(http_client)
    assert 'request' in methods

def test_can_raw_request_to_snap():
    http_client = HttpClient()
    response_dict, response_object = http_client.request(method='post',
        server_key='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA',
        request_url='https://app.sandbox.midtrans.com/snap/v1/transactions',
        parameters=generate_param_min())
    assert isinstance(response_dict, dict)
    assert is_str(response_dict['token'])

def test_fail_request_401_to_snap():
    http_client = HttpClient()
    err = ''
    try:
        response_dict, response_object = http_client.request(method='post',
            server_key='wrong-server-key',
            request_url='https://app.sandbox.midtrans.com/snap/v1/transactions',
            parameters=generate_param_min())
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert is_str(err.message)
    assert isinstance(err.api_response_dict, dict)
    assert 401 == err.http_status_code

def test_response_not_json_exception():
    http_client = HttpClient()
    try:
        response = http_client.request(method='post',
            server_key='',
            request_url='https://midtrans.com/',
            parameters='')
    except Exception as e:
        assert 'JSONDecodeError' in repr(e)

def test_is_custom_headers_applied():
    http_client = HttpClient()

    custom_headers = {
        'X-Override-Notification':'https://example.org'
    }

    # Mock requests
    with patch('requests.request') as mock_request:
        # Set status code to 200 to prevent MidtransAPIError
        mock_request.return_value.status_code = 200 

        # Trigger request
        http_client.request(method='post',
        server_key='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA',
        request_url='https://app.sandbox.midtrans.com/snap/v1/transactions',
        parameters=generate_param_min(),
        custom_headers=custom_headers)

        # Fetch the headers from requests.request arguments
        headers = mock_request.call_args[1]['headers']
        
        # Make sure default header still exist
        assert headers.get('content-type') == 'application/json'

        # Assert custom headers
        assert 'X-Override-Notification' in headers
        assert headers.get('X-Override-Notification') == 'https://example.org'

# TODO test GET request

# ======== HELPER FUNCTIONS BELOW ======== #
def generate_param_min():
    return {
        "transaction_details": {
            "order_id": "py-midtransclient-test-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gross_amount": 200000
        }, "credit_card":{
            "secure" : True
        }
    }