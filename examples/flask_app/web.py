import uuid
import json
from flask import Flask, render_template, request

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
    transaction_token = snap.create_transaction_token({
        "transaction_details": {
            "order_id": str(uuid.uuid4()),
            "gross_amount": 200000
        }, "credit_card":{
            "secure" : True
        }
    })
    return render_template('simple_checkout.html', 
        token = transaction_token, 
        client_key = snap.api_config.client_key)



#==============#
# Using Core API
#==============#

# Very simple core API
core = CoreApi(
    is_production=False,
    server_key='SB-Mid-server-GwUP_WGbJPXsDzsNEBRs8IYA',
    client_key='SB-Mid-client-61XuGAwQ8Bj8LxSS',
)
# Get Credit Card token via Frontend, then pass to token_id to `/process_core_api`
@app.route('/simple_core_api_checkout')
def simple_core_api_checkout():
    return render_template('simple_core_api_checkout.html', 
        client_key = core.api_config.client_key)

# Charge Credit Card token
@app.route('/process_core_api', methods=['POST'])
def process_core_api():
    api_response = core.charge({
        "payment_type": "credit_card",
        "transaction_details": {
            "gross_amount": 200000,
            "order_id": str(uuid.uuid4()),
        },
        "credit_card":{
            "token_id": request.form['token_id']
        }
    })
    return 'API response:<br><pre>{0}</pre>'\
        .format(json.dumps(api_response, indent=4))


#==============#
# Run Flask app
#==============#

# Homepage of this web app
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)