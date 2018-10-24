import midtransclient
# initialize core api client object
core = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# prepare CORE API parameter ( refer to: https://api-docs.midtrans.com ) charge bank_transfer parameter example
param = {
    "payment_type": "bank_transfer",
    "transaction_details": {
        "gross_amount": 24145,
        "order_id": "test-transaction-321",
    },
    "bank_transfer":{
        "bank": "bni"
    }
}

# charge transaction
charge_response = core.charge(param)
print('charge_response:')
print(charge_response)

# charge_response is dictionary representation of API JSON response
# sample:
# {
#     'currency': 'IDR',
#     'fraud_status': 'accept',
#     'gross_amount': '24145.00',
#     'order_id': 'test-transaction-321',
#     'payment_type': 'bank_transfer',
#     'status_code': '201',
#     'status_message': 'Success, Bank Transfer transaction is created',
#     'transaction_id': '6ee793df-9b1d-4343-8eda-cc9663b4222f',
#     'transaction_status': 'pending',
#     'transaction_time': '2018-10-24 15:34:33',
#     'va_numbers': [{'bank': 'bca', 'va_number': '490526303019299'}]
# }
