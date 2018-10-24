import midtransclient

# initialize api client object
api_client = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

mock_notification = {
    'currency': 'IDR',
    'fraud_status': 'accept',
    'gross_amount': '24145.00',
    'order_id': 'test-transaction-321',
    'payment_type': 'bank_transfer',
    'status_code': '201',
    'status_message': 'Success, Bank Transfer transaction is created',
    'transaction_id': '6ee793df-9b1d-4343-8eda-cc9663b4222f',
    'transaction_status': 'pending',
    'transaction_time': '2018-10-24 15:34:33',
    'va_numbers': [{'bank': 'bca', 'va_number': '490526303019299'}]
}
# handle notification JSON sent by Midtrans, it auto verify it by doing get status
# parameter can be Dictionary or String of JSON
status_response = api_client.transactions.notification(mock_notification)

order_id = status_response['order_id']
transaction_status = status_response['transaction_status']
fraud_status = status_response['fraud_status']

print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {2}'.format(order_id,
        transaction_status,
        fraud_status))

# Sample transaction_status handling logic

if transaction_status == 'capture':
    if fraud_status == 'challenge':
        # TODO set transaction status on your databaase to 'challenge'
        None
    elif fraud_status == 'accept':
        # TODO set transaction status on your databaase to 'success'
        None
elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
    # TODO set transaction status on your databaase to 'failure'
    None
elif transaction_status == 'pending':
    # TODO set transaction status on your databaase to 'pending' / waiting payment
    None
