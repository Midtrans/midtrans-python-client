# This is just for very basic implementation reference, in production, you should validate the incoming requests and implement your backend more securely.
import midtransclient
import datetime

# Initialize core api client object
# You can find it in Merchant Portal -> Settings -> Access keys
subscription = midtransclient.Subscription(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# prepare subscription parameter ( refer to: https://api-docs.midtrans.com/#create-subscription )
param = {
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

# create subscription
create_subscription = subscription.create(param)
print('create_subscription_response:')
print(create_subscription)

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

subscription_id = create_subscription['id']

# get subscription by subscription_id
get_subscription = subscription.get(subscription_id)
print('get_subscription_response:')
print(get_subscription)

# disable subscription by subscription_id
disable_subscription = subscription.disable(subscription_id)
print('disable_subscription_response:')
print(disable_subscription)

# enable subscription by subscription_id
enable_subscription = subscription.enable(subscription_id)
print('enable_subscription_response:')
print(enable_subscription)

# update subscription by subscription_id
update_param = {
    "name": "SUBS-PY-UPDATE",
}
update_subscription = subscription.update(subscription_id, update_param)
print('update_subscription_response:')
print(update_subscription)