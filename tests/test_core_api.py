import pytest
from .helpers import is_str
from .context import midtransclient
import datetime
import json
from pprint import pprint

USED_SERVER_KEY='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA'
USED_CLIENT_KEY='SB-Mid-client-61XuGAwQ8Bj8LxSS'

REUSED_ORDER_ID = [
    "py-midtransclient-test1-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
    "py-midtransclient-test2-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
    "py-midtransclient-test3-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
]
CC_TOKEN = ''
SAVED_CC_TOKEN = ''
API_RESPONSE = ''

def test_core_api_class():
    core = generate_core_api_instance()
    methods = dir(core)
    assert "charge" in methods
    assert is_str(core.api_config.server_key)
    assert is_str(core.api_config.client_key)

def test_core_api_card_token():
    core = generate_core_api_instance()
    params = {
        'card_number': '5264 2210 3887 4659',
        'card_exp_month': '12',
        'card_exp_year': '2030',
        'card_cvv': '123',
        'client_key': core.api_config.client_key,
    }
    response = core.card_token(params)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    global CC_TOKEN
    CC_TOKEN = response['token_id']
    assert is_str(response['token_id'])

def test_core_api_card_register():
    core = generate_core_api_instance()
    params = {
        'card_number': '4811 1111 1111 1114',
        'card_exp_month': '12',
        'card_exp_year': '2030',
        'card_cvv': '123',
        'client_key': core.api_config.client_key,
    }
    response = core.card_register(params)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    global SAVED_CC_TOKEN
    SAVED_CC_TOKEN = response['saved_token_id']
    assert is_str(response['saved_token_id'])

def test_core_api_card_point_inquiry_fail_402():
    core = generate_core_api_instance()
    try:
        response = core.card_point_inquiry(CC_TOKEN)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '402' in err.message


def test_core_api_charge_cc_simple():
    core = generate_core_api_instance()
    parameters = generate_param_cc_min(order_id=REUSED_ORDER_ID[1],cc_token=CC_TOKEN)
    response = core.charge(parameters)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    assert response['transaction_status'] == 'capture'
    assert response['fraud_status'] == 'accept'

def test_core_api_charge_cc_one_click():
    core = generate_core_api_instance()
    parameters = generate_param_cc_min(order_id=REUSED_ORDER_ID[2],cc_token=SAVED_CC_TOKEN)
    response = core.charge(parameters)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    assert response['transaction_status'] == 'capture'
    assert response['fraud_status'] == 'accept'

def test_core_api_charge_bank_transfer_bca_simple():
    core = generate_core_api_instance()
    parameters = generate_param_min(REUSED_ORDER_ID[0])
    response = core.charge(parameters)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 201
    assert response['transaction_status'] == 'pending'

def test_core_api_status():
    core = generate_core_api_instance()
    response = core.transactions.status(REUSED_ORDER_ID[0])
    global API_RESPONSE
    API_RESPONSE = response
    assert isinstance(response, dict)
    assert int(response['status_code']) == 201
    assert response['transaction_status'] == 'pending'

# TODO test statusb2b

def test_core_api_notification_from_dict():
    core = generate_core_api_instance()
    response = core.transactions.notification(API_RESPONSE)
    assert isinstance(response, dict)
    assert int(response['status_code']) == 201
    assert response['transaction_status'] == 'pending'

def test_core_api_notification_from_json():
    core = generate_core_api_instance()
    response = core.transactions.notification(json.dumps(API_RESPONSE))
    assert isinstance(response, dict)
    assert int(response['status_code']) == 201
    assert response['transaction_status'] == 'pending'

def test_core_api_notification_from_json_fail():
    core = generate_core_api_instance()
    err = ''
    try:
        response = core.transactions.notification('')
    except Exception as e:
        err = e
    assert 'JSONDecodeError' in repr(err)

def test_core_api_expire():
    core = generate_core_api_instance()
    response = core.transactions.expire(REUSED_ORDER_ID[0])
    assert isinstance(response, dict)
    assert int(response['status_code']) == 407
    assert response['transaction_status'] == 'expire'

def test_core_api_approve_fail_cannot_be_updated():
    core = generate_core_api_instance()
    err = ''
    try:
        response = core.transactions.approve(REUSED_ORDER_ID[1])
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '412' in err.message

def test_core_api_deny_cannot_be_updated():
    core = generate_core_api_instance()
    err = ''
    try:
        response = core.transactions.deny(REUSED_ORDER_ID[1])
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '412' in err.message

def test_core_api_cancel():
    core = generate_core_api_instance()
    response = core.transactions.cancel(REUSED_ORDER_ID[1])
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    assert response['transaction_status'] == 'cancel'

def test_core_api_refund_fail_not_yet_settlement():
    core = generate_core_api_instance()
    params = {
        "refund_key": "order1-ref1",
        "amount": 5000,
        "reason": "for some reason"
    }
    err = ''
    try:
        response = core.transactions.refund(REUSED_ORDER_ID[2],params)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '412' in err.message

def test_core_api_direct_refund_fail_not_yet_settlement():
    core = generate_core_api_instance()
    params = {
        "refund_key": "order1-ref1",
        "amount": 5000,
        "reason": "for some reason"
    }
    err = ''
    try:
        response = core.transactions.refundDirect(REUSED_ORDER_ID[2],params)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '412' in err.message

def test_core_api_status_fail_404():
    core = generate_core_api_instance()
    err = ''
    try:
        response = core.transactions.status('non-exist-order-id')
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '404' in err.message
    assert 'exist' in err.message

def test_core_api_status_server_key_change_via_property():
    core = midtransclient.CoreApi(is_production=False,server_key='',client_key='')
    core.api_config.server_key = USED_SERVER_KEY
    response = core.transactions.status(REUSED_ORDER_ID[1])
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    assert response['transaction_status'] == 'cancel'

def test_core_api_status_server_key_change_via_setter():
    core = midtransclient.CoreApi(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key='')
    assert core.api_config.is_production == False
    assert core.api_config.server_key == USED_SERVER_KEY
    try:
        response = core.transactions.status('non-exist-order-id')
    except Exception as e:
        assert '404' in e.message

    core.api_config.set(is_production=True,
        server_key='abc')
    assert core.api_config.is_production == True
    assert core.api_config.server_key == 'abc'
    try:
        response = core.transactions.status(REUSED_ORDER_ID[0])
    except Exception as e:
        assert '401' in e.message

    core.api_config.set(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key=USED_CLIENT_KEY)
    assert core.api_config.is_production == False
    assert core.api_config.server_key == USED_SERVER_KEY
    assert core.api_config.client_key == USED_CLIENT_KEY
    response = core.transactions.status(REUSED_ORDER_ID[1])
    assert isinstance(response, dict)
    assert int(response['status_code']) == 200
    assert response['transaction_status'] == 'cancel'

def test_core_api_charge_fail_401():
    core = generate_core_api_instance()
    core.api_config.server_key='invalidkey'
    parameters = generate_param_min()
    err = ''
    try:
        response = core.charge(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '401' in err.message
    assert 'authorized' in err.message

def test_core_api_charge_fail_empty_param():
    core = generate_core_api_instance()
    parameters = None
    err = ''
    try:
        response = core.charge(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '500' in err.message
    assert 'unexpected' in err.message

def test_core_api_charge_fail_zero_gross_amount():
    core = generate_core_api_instance()
    parameters = generate_param_min()
    parameters['transaction_details']['gross_amount'] = 0
    err = ''
    try:
        response = core.charge(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '400' in err.message

def test_core_api_exception_MidtransAPIError():
    core = generate_core_api_instance()
    err = ''
    try:
        response = core.transactions.status('non-exist-order-id')
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert is_str(err.message)
    assert isinstance(err.api_response_dict, dict)
    assert isinstance(err.http_status_code,int)

# ======== HELPER FUNCTIONS BELOW ======== #
def generate_core_api_instance():
    core_api = midtransclient.CoreApi(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key=USED_CLIENT_KEY)
    return core_api

def generate_param_min(order_id=None):
    return {
        "payment_type": "bank_transfer",
        "transaction_details": {
            "gross_amount": 44145,
            "order_id": "py-midtransclient-test-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if order_id == None else order_id,
        },
        "bank_transfer":{
            "bank": "bca"
        }
    }

def generate_param_cc_min(order_id=None,cc_token=None):
    return {
        "payment_type": "credit_card",
        "transaction_details": {
            "gross_amount": 12145,
            "order_id": "py-midtransclient-test-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if order_id == None else order_id,
        },
        "credit_card":{
            "token_id": cc_token
        }
    }

def generate_param_max():
    return {}