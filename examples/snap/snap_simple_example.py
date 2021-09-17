import midtransclient
# This is just for very basic implementation reference, in production, you should validate the incoming requests and implement your backend more securely.
# Please refer to this docs for snap popup:
# https://docs.midtrans.com/en/snap/integration-guide?id=integration-steps-overview

# Please refer to this docs for snap-redirect:
# https://docs.midtrans.com/en/snap/integration-guide?id=alternative-way-to-display-snap-payment-page-via-redirect

# initialize snap client object
# can find in Merchant Portal -> Settings -> Access keys
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# prepare SNAP API parameter ( refer to: https://snap-docs.midtrans.com ) minimum parameter example
param = {
    "transaction_details": {
        "order_id": "test-transaction-123",
        "gross_amount": 200000
    }, "credit_card":{
        "secure" : True
    }
}

# create transaction
transaction = snap.create_transaction(param)

# transaction token
transaction_token = transaction['token']
print('transaction_token:')
print(transaction_token)

# transaction redirect url
transaction_redirect_url = transaction['redirect_url']
print('transaction_redirect_url:')
print(transaction_redirect_url)

# transaction is dictionary representation of API JSON response
# sample:
# {
#   'redirect_url': 'https://app.sandbox.midtrans.com/snap/v2/vtweb/f0a2cbe7-dfb7-4114-88b9-1ecd89e90121', 
#   'token': 'f0a2cbe7-dfb7-4114-88b9-1ecd89e90121'
# }