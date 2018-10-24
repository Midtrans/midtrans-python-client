import midtransclient

# initialize api client object
api_client = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# These are wrapper/implementation of API methods described on: https://api-docs.midtrans.com/#midtrans-api

# get status of transaction that already recorded on midtrans (already `charge`-ed) 
status_response = api_client.transactions.status('YOUR_ORDER_ID OR TRANSACTION_ID')

# get transaction status of VA b2b transaction
statusb2b_response = api_client.transactions.statusb2b('YOUR_ORDER_ID OR TRANSACTION_ID')

# approve a credit card transaction with `challenge` fraud status
approve_response = api_client.transactions.approve('YOUR_ORDER_ID OR TRANSACTION_ID')

# deny a credit card transaction with `challenge` fraud status
deny_response = api_client.transactions.deny('YOUR_ORDER_ID OR TRANSACTION_ID')

# cancel a credit card transaction or pending transaction
cancel_response = api_client.transactions.cancel('YOUR_ORDER_ID OR TRANSACTION_ID')

# expire a pending transaction
expire_response = api_client.transactions.expire('YOUR_ORDER_ID OR TRANSACTION_ID')

# refund a transaction (not all payment channel allow refund via API)
param = {
    "amount": 5000,
    "reason": "Item out of stock"
}
refund_response = api_client.transactions.refund('YOUR_ORDER_ID OR TRANSACTION_ID',param)