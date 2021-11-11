import pytest
from .config import USED_SERVER_KEY, USED_CLIENT_KEY
from .helpers import is_str
from .context import midtransclient
import datetime
import json
from pprint import pprint

SUBSCRIPTION_ID = ''

def test_subscription_class():
    subscription = generate_subscription_instance()
    methods = dir(subscription)
    assert "create_subscription" in methods
    assert is_str(subscription.api_config.server_key)
    assert is_str(subscription.api_config.client_key)

def test_subscription_create_subscription():
    subscription = generate_subscription_instance()
    parameters = generate_param()
    response = subscription.create_subscription(parameters)
    global SUBSCRIPTION_ID
    SUBSCRIPTION_ID = response['id']
    assert isinstance(response, dict)
    assert 'id' in response.keys()
    assert response['status'] == 'active'

def test_subscription_fail_empty_param():
    subscription = generate_subscription_instance()
    parameters = None
    err = ''
    try:
        response = subscription.create_subscription(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '400' in err.message
    assert 'Bad request' in err.message

def test_subscription_fail_zero_amount():
    subscription = generate_subscription_instance()
    parameters = generate_param()
    parameters['amount'] = 0
    err = ''
    try:
        response = subscription.create_subscription(parameters)
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '400' in err.message
    assert 'subscription.amount must be between 0.01 - 99999999999.00' in err.message

def test_subscription_get_subscription():
    subscription = generate_subscription_instance()
    parameters = generate_param()
    response = subscription.get_subscription(SUBSCRIPTION_ID)
    assert isinstance(response, dict)
    assert response['id'] == SUBSCRIPTION_ID
    assert response['status'] == 'active'

def test_subscription_get_subscription_not_found():
    subscription = generate_subscription_instance()
    err = ''
    try:
        response = subscription.get_subscription('123')
    except Exception as e:
        err = e
    assert 'MidtransAPIError' in err.__class__.__name__
    assert '404' in err.message
    assert 'Subscription doesn\'t exist.' in err.message

def test_subscription_disable_subscription():
    subscription = generate_subscription_instance()
    response = subscription.disable_subscription(SUBSCRIPTION_ID)
    assert isinstance(response, dict)
    assert response['status_message'] == 'Subscription is updated.'
    get_subscription = subscription.get_subscription(SUBSCRIPTION_ID)
    assert get_subscription['id'] == SUBSCRIPTION_ID
    assert get_subscription['status'] == 'inactive'

def test_subscription_enable_subscription():
    subscription = generate_subscription_instance()
    response = subscription.enable_subscription(SUBSCRIPTION_ID)
    assert isinstance(response, dict)
    assert response['status_message'] == 'Subscription is updated.'
    get_subscription = subscription.get_subscription(SUBSCRIPTION_ID)
    assert get_subscription['id'] == SUBSCRIPTION_ID
    assert get_subscription['status'] == 'active'
    # disable subscription to prevent Core API continue to execute subscription
    response = subscription.disable_subscription(SUBSCRIPTION_ID)

def test_subscription_update_subscription():
    subscription = generate_subscription_instance()
    parameters = generate_param()
    parameters['metadata']['description'] = 'update recurring payment to ABC'
    response = subscription.update_subscription(SUBSCRIPTION_ID,parameters)
    assert isinstance(response, dict)
    assert response['status_message'] == 'Subscription is updated.'
    get_subscription = subscription.get_subscription(SUBSCRIPTION_ID)
    assert get_subscription['id'] == SUBSCRIPTION_ID
    assert get_subscription['metadata']['description'] == 'update recurring payment to ABC'

# ======== HELPER FUNCTIONS BELOW ======== #
def generate_subscription_instance():
    subscription = midtransclient.CoreApi(is_production=False,
        server_key=USED_SERVER_KEY,
        client_key=USED_CLIENT_KEY)
    return subscription

def generate_param():
    return {
        "name": "SUBS-PY-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
        "amount": "100000",
        "currency": "IDR",
        "payment_type": "credit_card",
        "token": "436502qFfqfAQKScMtPRPdZDOaeg7199",
        "schedule": {
          "interval": 1,
          "interval_unit": "day",
          "max_interval": 7
        },
        "metadata": {
          "description": "Recurring payment for A"
        },
        "customer_details": {
          "first_name": "John A",
          "last_name": "Doe A",
          "email": "johndoe@email.com",
          "phone": "+62812345678"
        }
    }
