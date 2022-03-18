import pytest
from .config import USED_SERVER_KEY, USED_CLIENT_KEY
from .helpers import is_str
from .context import midtransclient
import datetime
from pprint import pprint

reused_order_id = "py-midtransclient-test-"+str(datetime.datetime.now()).replace(" ", "").replace(":", "")

def test_snap_class():
    snap = generate_snap_instance()
    methods = dir(snap)
    assert "create_transaction" in methods
    assert "create_transaction_token" in methods
    assert "create_transaction_redirect_url" in methods
    assert is_str(snap.api_config.server_key)
    assert is_str(snap.api_config.client_key)

def test_snap_create_transaction_min():
    snap = generate_snap_instance()
    param = generate_param_min()
    param['transaction_details']['order_id'] = reused_order_id
    transaction = snap.create_transaction(param)
    assert isinstance(transaction, dict)
    assert is_str(transaction['token'])
    assert is_str(transaction['redirect_url'])

def test_snap_create_transaction_max():
    snap = generate_snap_instance()
    param = generate_param_max()
    transaction = snap.create_transaction(param)
    assert isinstance(transaction, dict)
    assert is_str(transaction['token'])
    assert is_str(transaction['redirect_url'])

def test_snap_create_transaction_token():
    snap = generate_snap_instance()
    param = generate_param_min()
    token = snap.create_transaction_token(param)
    assert is_str(token)

def test_snap_create_transaction_redirect_url():
    snap = generate_snap_instance()
    param = generate_param_min()
    redirect_url = snap.create_transaction_redirect_url(param)
    assert is_str(redirect_url)

def test_snap_status_fail_404():
    snap = generate_snap_instance()
    err = ''
    try:
        response = snap.transactions.status('non-exist-order-id')
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '404' in err.message
    assert 'exist' in err.message

def test_snap_request_fail_401():
    snap = generate_snap_instance()
    snap.api_config.server_key='dummy'
    param = generate_param_min()
    err = ''
    try:
        transaction = snap.create_transaction(param)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '401' in err.message
    assert 'unauthorized' in err.message

def test_snap_request_fail_empty_param():
    snap = generate_snap_instance()
    param = None
    err = ''
    try:
        transaction = snap.create_transaction(param)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '400' in err.message
    assert 'is required' in err.message

def test_snap_request_fail_zero_gross_amount():
    snap = generate_snap_instance()
    param = generate_param_min()
    param['transaction_details']['gross_amount'] = 0
    err = ''
    try:
        transaction = snap.create_transaction(param)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__

def test_snap_exception_MidtransAPIError():
    snap = generate_snap_instance()
    snap.api_config.server_key='dummy'
    param = generate_param_min()
    err = ''
    try:
        transaction = snap.create_transaction(param)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert is_str(err.message)
    assert isinstance(err.api_response_dict, dict)
    assert isinstance(err.http_status_code,int)

def test_snap_create_transaction_min_with_custom_headers_via_setter():
    snap = generate_snap_instance()
    snap.api_config.custom_headers = {
        'X-Override-Notification':'https://example.org'
    }
    param = generate_param_min()
    param['transaction_details']['order_id'] = reused_order_id
    transaction = snap.create_transaction(param)
    assert isinstance(transaction, dict)
    assert is_str(transaction['token'])
    assert is_str(transaction['redirect_url'])

# ======== HELPER FUNCTIONS BELOW ======== #
def generate_snap_instance():
    snap = midtransclient.Snap(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key=USED_CLIENT_KEY)
    return snap

def generate_param_min():
    return {
        "transaction_details": {
            "order_id": "py-midtransclient-test-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gross_amount": 200000
        }, "credit_card":{
            "secure" : True
        }
    }

def generate_param_max():
    return {
        "transaction_details": {
            "order_id": "py-midtransclient-test-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gross_amount": 10000
        },
        "item_details": [{
            "id": "ITEM1",
            "price": 10000,
            "quantity": 1,
            "name": "Midtrans Bear",
            "brand": "Midtrans",
            "category": "Toys",
            "merchant_name": "Midtrans"
        }],
        "customer_details": {
            "first_name": "John",
            "last_name": "Watson",
            "email": "test@example.com",
            "phone": "+628123456",
            "billing_address": {
                "first_name": "John",
                "last_name": "Watson",
                "email": "test@example.com",
                "phone": "081 2233 44-55",
                "address": "Sudirman",
                "city": "Jakarta",
                "postal_code": "12190",
                "country_code": "IDN"
            },
            "shipping_address": {
                "first_name": "John",
                "last_name": "Watson",
                "email": "test@example.com",
                "phone": "0 8128-75 7-9338",
                "address": "Sudirman",
                "city": "Jakarta",
                "postal_code": "12190",
                "country_code": "IDN"
            }
        },
        "enabled_payments": ["credit_card", "mandiri_clickpay", "cimb_clicks","bca_klikbca", "bca_klikpay", "bri_epay", "echannel", "indosat_dompetku","mandiri_ecash", "permata_va", "bca_va", "bni_va", "other_va", "gopay","kioson", "indomaret", "gci", "danamon_online"],
        "credit_card": {
            "secure": True,
            "channel": "migs",
            "bank": "bca",
            "installment": {
                "required": False,
                "terms": {
                    "bni": [3, 6, 12],
                    "mandiri": [3, 6, 12],
                    "cimb": [3],
                    "bca": [3, 6, 12],
                    "offline": [6, 12]
                }
            },
            "whitelist_bins": [
                "48111111",
                "41111111"
            ]
        },
        "bca_va": {
            "va_number": "12345678911",
            "free_text": {
                "inquiry": [
                    {
                        "en": "text in English",
                        "id": "text in Bahasa Indonesia"
                    }
                ],
                "payment": [
                    {
                        "en": "text in English",
                        "id": "text in Bahasa Indonesia"
                    }
                ]
            }
        },
        "bni_va": {
            "va_number": "12345678"
        },
        "permata_va": {
            "va_number": "1234567890",
            "recipient_name": "SUDARSONO"
        },
        "callbacks": {
            "finish": "https://demo.midtrans.com"
        },
        "expiry": {
            "start_time": "2030-12-20 18:11:08 +0700",
            "unit": "minutes",
            "duration": 1
        },
        "custom_field1": "custom field 1 content",
        "custom_field2": "custom field 2 content",
        "custom_field3": "custom field 3 content"
    }