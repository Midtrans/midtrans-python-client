import midtransclient
# initialize core api client object
core = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# Alternative way to initialize CoreApi client object:
# core = midtransclient.CoreApi()
# core.api_config.set(
#     is_production=False,
#     server_key='YOUR_SERVER_KEY',
#     client_key='YOUR_CLIENT_KEY'
# )

# Another alternative way to initialize CoreApi client object:
# core = midtransclient.CoreApi()
# core.api_config.is_production=False
# core.api_config.server_key='YOUR_SERVER_KEY'
# core.api_config.client_key='YOUR_CLIENT_KEY'

# IMPORTANT NOTE: You should do credit card get token via frontend using `midtrans.min.js`, to avoid card data breach risks on your backend
# ( refer to: https://api-docs.midtrans.com )

# prepare CORE API parameter to get credit card token
params = {
    'card_number': '5264 2210 3887 4659',
    'card_exp_month': '12',
    'card_exp_year': '2020',
    'card_cvv': '123',
    'client_key': core.api_config.client_key,
}
card_token_response = core.card_token(params)
cc_token = card_token_response['token_id']

# prepare CORE API parameter to charge credit card ( refer to: https://api-docs.midtrans.com )
param = {
    "payment_type": "credit_card",
    "transaction_details": {
        "gross_amount": 12145,
        "order_id": "test-transaction-54321",
    },
    "credit_card":{
        "token_id": cc_token
    }
}

# charge transaction
charge_response = core.charge(param)
print('charge_response:')
print(charge_response)

# charge_response is dictionary representation of API JSON response
# sample:
# {
#     'approval_code': '1540370521462',
#     'bank': 'bni',
#     'card_type': 'debit',
#     'channel_response_code': '00',
#     'channel_response_message': 'Approved',
#     'currency': 'IDR',
#     'fraud_status': 'accept',
#     'gross_amount': '12145.00',
#     'masked_card': '526422-4659',
#     'order_id': 'test-transaction-54321',
#     'payment_type': 'credit_card',
#     'status_code': '200',
#     'status_message': 'Success, Credit Card transaction is successful',
#     'transaction_id': '2bc57149-b52b-46ff-b901-86418ad1abcc',
#     'transaction_status': 'capture',
#     'transaction_time': '2018-10-24 15:42:01'
# }
