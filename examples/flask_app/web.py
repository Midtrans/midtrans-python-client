import datetime
import json
from flask import Flask, render_template, request, jsonify

from midtransclient import Snap, CoreApi

app = Flask(__name__)

#==============#
# Using SNAP
#==============#

# Very simple Snap checkout
@app.route('/simple_checkout')
def simple_checkout():
    snap = Snap(
        is_production=False,
        server_key='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA',
        client_key='SB-Mid-client-61XuGAwQ8Bj8LxSS',
    )
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_token = snap.create_transaction_token({
        "transaction_details": {
            "order_id": "order-id-python-"+timestamp,
            "gross_amount": 200000
        }, "credit_card":{
            "secure" : True
        }
    })
    return render_template('simple_checkout.html', 
        token = transaction_token, 
        client_key = snap.api_config.client_key)


#==============#
# Using Core API - Credit Card
#==============#

# [0] Setup API client and config
core = CoreApi(
    is_production=False,
    server_key='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA',
    client_key='SB-Mid-client-61XuGAwQ8Bj8LxSS',
)
# [1] Render HTML+JS web page to get card token_id and [3] 3DS authentication
@app.route('/simple_core_api_checkout')
def simple_core_api_checkout():
    return render_template('simple_core_api_checkout.html', 
        client_key = core.api_config.client_key)

# [2] Handle Core API credit card token_id charge
@app.route('/charge_core_api_ajax', methods=['POST'])
def charge_core_api_ajax():
    request_json = request.get_json()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        charge_api_response = core.charge({
            "payment_type": "credit_card",
            "transaction_details": {
                "gross_amount": 200000,
                "order_id": "order-id-python-"+timestamp,
            },
            "credit_card":{
                "token_id": request_json['token_id'],
                "authentication": request_json['authenticate_3ds'],
            }
        })
    except Exception as e:
        charge_api_response = e.api_response_dict
    return charge_api_response

# [4] Handle Core API check transaction status
@app.route('/check_transaction_status', methods=['POST'])
def check_transaction_status():
    request_json = request.get_json()
    transaction_status = core.transactions.status(request_json['transaction_id'])

    # [5.A] Handle transaction status on your backend
    # Sample transaction_status handling logic
    if transaction_status == 'capture':
        if fraud_status == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            None
        elif fraud_status == 'accept':
            # TODO set transaction status on your databaase to 'success'
            None
    elif transaction_status == 'settlement':
        # TODO set transaction status on your databaase to 'success'
        # Note: Non-card transaction will become 'settlement' on payment success
        # Card transaction will also become 'settlement' D+1, which you can ignore
        # because most of the time 'capture' is enough to be considered as success
        None
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # TODO set transaction status on your databaase to 'failure'
        None
    elif transaction_status == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        None
    elif transaction_status == 'refund':
        # TODO set transaction status on your databaase to 'refund'
        None
    return jsonify(transaction_status)

#==============#
# Handling HTTP Post Notification
#==============#

# [4] Handle Core API check transaction status
@app.route('/notification_handler', methods=['POST'])
def notification_handler():
    request_json = request.get_json()
    transaction_status_dict = core.transactions.notification(request_json)

    order_id           = request_json['order_id']
    transaction_status = request_json['transaction_status']
    fraud_status       = request_json['fraud_status']
    transaction_json   = json.dumps(transaction_status_dict)

    summary = 'Transaction notification received. Order ID: {order_id}. Transaction status: {transaction_status}. Fraud status: {fraud_status}.<br>Raw notification object:<pre>{transaction_json}</pre>'.format(order_id=order_id,transaction_status=transaction_status,fraud_status=fraud_status,transaction_json=transaction_json)

    # [5.B] Handle transaction status on your backend
    # Sample transaction_status handling logic
    if transaction_status == 'capture':
        if fraud_status == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            None
        elif fraud_status == 'accept':
            # TODO set transaction status on your databaase to 'success'
            None
    elif transaction_status == 'settlement':
        # TODO set transaction status on your databaase to 'success'
        # Note: Non card transaction will become 'settlement' on payment success
        # Credit card will also become 'settlement' D+1, which you can ignore
        # because most of the time 'capture' is enough to be considered as success
        None
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # TODO set transaction status on your databaase to 'failure'
        None
    elif transaction_status == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        None
    elif transaction_status == 'refund':
        # TODO set transaction status on your databaase to 'refund'
        None
    app.logger.info(summary)
    return jsonify(summary)

#==============#
# Using Core API - other payment method, example: Permata VA
#==============#
@app.route('/simple_core_api_checkout_permata', methods=['GET'])
def simple_core_api_checkout_permata():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    charge_api_response = core.charge({
        "payment_type": "bank_transfer",
        "transaction_details": {
            "gross_amount": 200000,
            "order_id": "order-id-python-"+timestamp,
        }
    })
    
    return render_template('simple_core_api_checkout_permata.html', 
        permata_va_number = charge_api_response['permata_va_number'],
        gross_amount = charge_api_response['gross_amount'],
        order_id = charge_api_response['order_id'])

#==============#
# Run Flask app
#==============#

# Homepage of this web app
@app.route('/')
def index():
    return render_template('index.html')
# credit card frontend demo
@app.route('/core_api_credit_card_frontend_sample')
def core_api_credit_card_frontend_sample():
    return render_template('core_api_credit_card_frontend_sample.html', 
        client_key = core.api_config.client_key)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')