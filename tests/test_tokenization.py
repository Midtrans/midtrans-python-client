import pytest
from .config import USED_SERVER_KEY, USED_CLIENT_KEY
from .helpers import is_str
from .context import midtransclient
import datetime
import json
from pprint import pprint

PHONEUNREGISTERED = "123450001"
PHONEBLOCKED = "123450002"
ACCOUNT_ID = ''

def test_tokenization_class():
    tokenization = generate_tokenization_instance()
    methods = dir(tokenization)
    assert "link_payment_account" in methods
    assert is_str(tokenization.api_config.server_key)
    assert is_str(tokenization.api_config.client_key)

def test_tokenization_link_account():
    tokenization = generate_tokenization_instance()
    parameters = generate_param('81234567891')
    response = tokenization.link_payment_account(parameters)
    global ACCOUNT_ID
    ACCOUNT_ID = response['account_id']
    assert isinstance(response, dict)
    assert 'account_id' in response.keys()
    assert response['status_code'] == '201'
    assert response['account_status'] == 'PENDING'

def test_tokenization_link_account_user_not_found():
    tokenization = generate_tokenization_instance()
    parameters = generate_param(PHONEUNREGISTERED)
    response = tokenization.link_payment_account(parameters)
    assert isinstance(response, dict)
    assert response['status_code'] == '202'
    assert response['channel_response_message'] == 'User Not Found'

def test_tokenization_link_account_user_blocked():
    tokenization = generate_tokenization_instance()
    parameters = generate_param(PHONEBLOCKED)
    response = tokenization.link_payment_account(parameters)
    assert isinstance(response, dict)
    assert response['status_code'] == '202'
    assert response['channel_response_message'] == 'Wallet is Blocked'

def test_tokenization_link_account_phone_start_with_0():
    tokenization = generate_tokenization_instance()
    parameters = generate_param('081234567891')
    err = ''
    try:
        response = tokenization.link_payment_account(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '400' in err.message
    assert 'gopay_partner.phone_number must be numeric digits and must not begin with 0' in err.message

def test_tokenization_get_account():
    tokenization = generate_tokenization_instance()
    response = tokenization.get_payment_account(ACCOUNT_ID)
    assert isinstance(response, dict)
    assert response['status_code'] == '201'
    assert response['account_id'] == ACCOUNT_ID

def test_tokenization_unlink_account():
    tokenization = generate_tokenization_instance()
    err = ''
    try:
        response = tokenization.unlink_payment_account(ACCOUNT_ID)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '412' in err.message
    assert 'Account status cannot be updated.' in err.message
    

# ======== HELPER FUNCTIONS BELOW ======== #
def generate_tokenization_instance():
    tokenization = midtransclient.CoreApi(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key=USED_CLIENT_KEY)
    return tokenization

def generate_param(phone_number):
    return {
      "payment_type": "gopay",
      "gopay_partner": {
        "phone_number": phone_number,
        "country_code": "62",
        "redirect_url": "https://mywebstore.com/gopay-linking-finish"
      }
    }
