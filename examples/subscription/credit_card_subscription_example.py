# This is just for very basic implementation reference, in production, you should validate the incoming requests and implement your backend more securely.
import midtransclient
import datetime

# Initialize core api client object
# You can find it in Merchant Portal -> Settings -> Access keys
core_api = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# To use API subscription for credit card, you should first obtain the 1 click token
# Refer to docs: https://docs.midtrans.com/en/core-api/advanced-features?id=recurring-transaction-with-subscriptions-api

# You will receive saved_token_id after complete 3ds authentication (it also available in the JSON of HTTP notification)
# Refer to docs: https://docs.midtrans.com/en/core-api/advanced-features?id=sample-3ds-authenticate-json-response-for-the-first-transaction
# {
#   ...
#   "card_type": "credit",
#   "saved_token_id":"481111xDUgxnnredRMAXuklkvAON1114",
#   "saved_token_id_expired_at": "2022-12-31 07:00:00",
#   ...
# }
# Sample saved token id for testing purpose
SAVED_TOKEN_ID = '436502qFfqfAQKScMtPRPdZDOaeg7199'

# prepare subscription parameter ( refer to: https://api-docs.midtrans.com/#create-subscription )
param = {
    "name": "SUBS-PY-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
    "amount": "100000",
    "currency": "IDR",
    "payment_type": "credit_card",
    "token": SAVED_TOKEN_ID,
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

# create subscription
create_subscription_response = core_api.create_subscription(param)
print('create_subscription_response:')
print(create_subscription_response)

# subscription_response is dictionary representation of API JSON response
# sample:
# {
#   'id': 'b6eb6a04-33e6-46a2-a298-cd78e55b3a3f',
#   'name': 'SUBS-PY-1',
#   'amount': '100000',
#   'currency': 'IDR',
#   'created_at': '2021-10-27 13:29:51',
#   'schedule': {
#     'interval': 1,
#     'current_interval': 0,
#     'max_interval': 7,
#     'interval_unit': 'day',
#     'start_time': '2021-10-27 13:30:01',
#     'next_execution_at': '2021-10-27 13:30:01'
#   },
#   'status': 'active',
#   'token': '436502qFfqfAQKScMtPRPdZDOaeg7199',
#   'payment_type': 'credit_card',
#   'transaction_ids': [
    
#   ],
#   'metadata': {
#     'description': 'Recurring payment for A'
#   },
#   'customer_details': {
#     'email': 'johndoe@email.com',
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'phone': '+62812345678'
#   }
# }

subscription_id_response = create_subscription_response['id']

# get subscription by subscription_id
get_subscription_response = core_api.get_subscription(subscription_id_response)
print('get_subscription_response:')
print(get_subscription_response)

# enable subscription by subscription_id
enable_subscription_response = core_api.enable_subscription(subscription_id_response)
print('enable_subscription_response:')
print(enable_subscription_response)

# update subscription by subscription_id
update_param = {
    "name": "SUBS-PY-UPDATE",
    "amount": "100000",
    "currency": "IDR",
    "token": SAVED_TOKEN_ID,
    "schedule": {
      "interval": 1
    }
}
update_subscription_response = core_api.update_subscription(subscription_id_response, update_param)
print('update_subscription_response:')
print(update_subscription_response)

# disable subscription by subscription_id
disable_subscription_response = core_api.disable_subscription(subscription_id_response)
print('disable_subscription_response:')
print(disable_subscription_response)
