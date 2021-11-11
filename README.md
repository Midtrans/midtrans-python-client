Midtrans Client - Python
===============

[![PyPI version](https://badge.fury.io/py/midtransclient.svg)](https://badge.fury.io/py/midtransclient)
[![Downloads](https://pepy.tech/badge/midtransclient/month)](https://pepy.tech/project/midtransclient)
[![Downloads](https://pepy.tech/badge/midtransclient)](https://pepy.tech/project/midtransclient)

Midtrans ❤️ Python! 🐍

This is the Official Python API client/library for Midtrans Payment API. Visit [https://midtrans.com](https://midtrans.com). More information about the product and see documentation at [http://docs.midtrans.com](https://docs.midtrans.com) for more technical details.

## 1. Installation

### 1.a Using Pip

```
pip install midtransclient
```

### 1.b Manual Installation

If you are not using Pip, you can clone or [download](https://github.com/midtrans/midtrans-python-client/archive/master.zip) this repository.
Then import from `midtransclient` folder.

Or run Pip install from the repo folder.
```
pip install .
```

## 2. Usage

### 2.1 Choose Product/Method

We have [2 different products](https://docs.midtrans.com/en/welcome/index.html) of payment that you can use:
- [Snap](#22A-snap) - Customizable payment popup will appear on **your web/app** (no redirection). [doc ref](https://snap-docs.midtrans.com/)
- [Snap Redirect](#22B-snap-redirect) - Customer need to be redirected to payment url **hosted by midtrans**. [doc ref](https://snap-docs.midtrans.com/)
- [Core API (VT-Direct)](#22C-core-api-vt-direct) - Basic backend implementation, you can customize the frontend embedded on **your web/app** as you like (no redirection). [doc ref](https://api-docs.midtrans.com/)

Choose one that you think best for your unique needs.

### 2.2 Client Initialization and Configuration

Get your client key and server key from [Midtrans Dashboard](https://dashboard.midtrans.com)

Create API client object

```python
# Create Core API instance
core_api = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
```


```python
# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
```

You can also re-set config using `Snap.api_config.set( ... )`
example:

```python

# initialize object, empty config
snap = midtransclient.Snap()

# re-set full config
snap.api_config.set(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# re-set server_key only
snap.api_config.set(server_key='YOUR_SERVER_KEY')

# re-set is_production only
snap.api_config.set(is_production=True)
```

You can also set config directly from attribute
```python
# initialize object, empty config
snap = midtransclient.Snap()

# set config
snap.api_config.is_production=False
snap.api_config.server_key='YOUR_SERVER_KEY'
snap.api_config.client='YOUR_CLIENT_KEY'
```


### 2.2.A Snap
You can see Snap example [here](examples/snap).

Available methods for `Snap` class
```python
# return Snap API /transaction response as Dictionary
def create_transactions(parameter):

# return Snap API /transaction token as String
def create_transactions_token(parameter):

# return Snap API /transaction redirect_url as String
def create_transactions_redirect_url(parameter):
```
`parameter` is Dictionary or String of JSON of [SNAP Parameter](https://snap-docs.midtrans.com/#json-objects)


#### Get Snap Token

```python
# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# Prepare parameter
param = {
    "transaction_details": {
        "order_id": "test-transaction-123",
        "gross_amount": 200000
    }, "credit_card":{
        "secure" : True
    }
}

transaction = snap.create_transaction(param)

transaction_token = transaction['token']
# alternative way to create transaction_token:
# transaction_token = snap.create_transaction_token(param)
```


#### Initialize Snap JS when customer click pay button

Replace `PUT_TRANSACTION_TOKEN_HERE` with `transaction_token` acquired above
```html
<html>
  <body>
    <button id="pay-button">Pay!</button>
    <pre><div id="result-json">JSON result will appear here after payment:<br></div></pre>

<!-- TODO: Remove ".sandbox" from script src URL for production environment. Also input your client key in "data-client-key" -->
    <script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="<Set your ClientKey here>"></script>
    <script type="text/javascript">
      document.getElementById('pay-button').onclick = function(){
        // SnapToken acquired from previous step
        snap.pay('PUT_TRANSACTION_TOKEN_HERE', {
          // Optional
          onSuccess: function(result){
            /* You may add your own js here, this is just example */ document.getElementById('result-json').innerHTML += JSON.stringify(result, null, 2);
          },
          // Optional
          onPending: function(result){
            /* You may add your own js here, this is just example */ document.getElementById('result-json').innerHTML += JSON.stringify(result, null, 2);
          },
          // Optional
          onError: function(result){
            /* You may add your own js here, this is just example */ document.getElementById('result-json').innerHTML += JSON.stringify(result, null, 2);
          }
        });
      };
    </script>
  </body>
</html>
```

#### Implement Notification Handler
[Refer to this section](#23-handle-http-notification)

### 2.2.B Snap Redirect

Also available as examples [here](examples/snap).

#### Get Redirection URL of a Payment Page

```python
# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# Prepare parameter
param = {
    "transaction_details": {
        "order_id": "test-transaction-123",
        "gross_amount": 200000
    }, "credit_card":{
        "secure" : True
    }
}

transaction = snap.create_transaction(param)

transaction_redirect_url = transaction['redirect_url']
# alternative way to create redirect_url:
# transaction_redirect_url = snap.create_redirect_url(param)
```
#### Implement Notification Handler
[Refer to this section](#23-handle-http-notification)

### 2.2.C Core API (VT-Direct)

You can see some Core API examples [here](examples/core_api).

Available methods for `CoreApi` class
```python
def charge(self,parameters=dict()):
    """
    Trigger `/charge` API call to Core API
    :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
    (more params detail refer to: https://api-docs.midtrans.com)

    :return: Dictionary from JSON decoded response
    """

def capture(self,parameters=dict()):
    """
    Trigger `/capture` API call to Core API
    Capture is only used for pre-authorize transaction only
    :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
    (more params detail refer to: https://api-docs.midtrans.com)

    :return: Dictionary from JSON decoded response
    """

def card_register(self,parameters=dict()):
    """
    Trigger `/card/register` API call to Core API
    :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
    (more params detail refer to: https://api-docs.midtrans.com)

    :return: Dictionary from JSON decoded response
    """

def card_token(self,parameters=dict()):
    """
    Trigger `/token` API call to Core API
    :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
    (more params detail refer to: https://api-docs.midtrans.com)

    :return: Dictionary from JSON decoded response
    """

def card_point_inquiry(self,token_id):
    """
    Trigger `/point_inquiry/<token-id>` API call to Core API
    :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
    (more params detail refer to: https://api-docs.midtrans.com)

    :return: Dictionary from JSON decoded response
    """
```
`parameter` is Dictionary or String of JSON of [Core API Parameter](https://api-docs.midtrans.com/#json-objects)

#### Credit Card Get Token

Get token should be handled on  Frontend please refer to [API docs](https://api-docs.midtrans.com)

#### Credit Card Charge

```python
# Create Core API instance
core_api = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# Prepare parameter
param = {
    "payment_type": "credit_card",
    "transaction_details": {
        "gross_amount": 12145,
        "order_id": "test-transaction-54321",
    },
    "credit_card":{
        "token_id": 'CREDIT_CARD_TOKEN', # change with your card token
        "authentication": True
    }
}

# charge transaction
charge_response = core_api.charge(param)
print('charge_response:')
print(charge_response)
```

#### Credit Card 3DS Authentication

The credit card charge result may contains `redirect_url` for 3DS authentication. 3DS Authentication should be handled on Frontend please refer to [API docs](https://api-docs.midtrans.com/#card-features-3d-secure)

For full example on Credit Card 3DS transaction refer to:
- [Flask App examples](/examples/flask_app) that implement Snap & Core Api

### 2.2.D Subscription API

You can see some Subscription API examples [here](examples/subscription), [Subscription API Docs](https://api-docs.midtrans.com/#subscription-api)

#### Subscription API for Credit Card

To use subscription API for credit card, you should first obtain the 1-click saved token, [refer to this docs.](https://docs.midtrans.com/en/core-api/advanced-features?id=recurring-transaction-with-subscriptions-api) 

You will receive `saved_token_id` as part of the response when the initial card payment is accepted (will also available in the HTTP notification's JSON), [refer to this docs.](https://docs.midtrans.com/en/core-api/advanced-features?id=sample-3ds-authenticate-json-response-for-the-first-transaction)

```python
# Create Subscription API instance
core_api = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# Prepare parameter
param = {
    "name": "SUBSCRIPTION-STARTER-1",
    "amount": "100000",
    "currency": "IDR",
    "payment_type": "credit_card",
    "token": "436502qFfqfAQKScMtPRPdZDOaeg7199",
    "schedule": {
      "interval": 1,
      "interval_unit": "month",
      "max_interval": 3,
      "start_time": "2021-10-01 07:25:01 +0700"
    },
    "metadata": {
      "description": "Recurring payment for STARTER 1"
    },
    "customer_details": {
      "first_name": "John A",
      "last_name": "Doe A",
      "email": "johndoe@email.com",
      "phone": "+62812345678"
    }
}
create_subscription_response = core_api.create_subscription(param)

subscription_id_response = create_subscription_response['id']
# get subscription by subscription_id
get_subscription_response = core_api.get_subscription(subscription_id_response)

# disable subscription by subscription_id
disable_subscription_response = core_api.disable_subscription(subscription_id_response)

# enable subscription by subscription_id
enable_subscription_response = core_api.enable_subscription(subscription_id_response)

# update subscription by subscription_id
update_param = {
    "name": "SUBSCRIPTION-STARTER-1-UPDATE",
    "amount": "100000",
    "currency": "IDR",
    "token": "436502qFfqfAQKScMtPRPdZDOaeg7199",
    "schedule": {
      "interval": 1
}
update_subscription_response = core_api.update_subscription(subscription_id_response, update_param)
```

#### Subscription API for Gopay

To use subscription API for gopay, you should first link your customer gopay account with gopay tokenization API, [refer to this section](#22e-tokenization-api)

You will receive gopay payment token using `get_payment_account` API call 

You can see some Subscription API examples [here](examples/subscription)

### 2.2.E Tokenization API
You can see some Tokenization API examples [here](examples/tokenization), [Tokenization API Docs](https://api-docs.midtrans.com/#gopay-tokenization)

```python
# Create Tokenization API instance
core_api = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# Prepare parameter
param = {
  "payment_type": "gopay",
  "gopay_partner": {
    "phone_number": "81234567891",
    "country_code": "62",
    "redirect_url": "https://mywebstore.com/gopay-linking-finish" #please update with your redirect URL
  }
}

# link payment account
link_payment_account_response = core_api.link_payment_account(param)

# get payment account
get_payment_account_response = core_api.get_payment_account(active_account_id)

# unlink account
unlink_payment_account_response = core_api.unlink_payment_account(active_account_id)
```

### 2.3 Handle HTTP Notification

> **IMPORTANT NOTE**: To update transaction status on your backend/database, **DO NOT** solely rely on frontend callbacks! For security reason to make sure the status is authentically coming from Midtrans, only update transaction status based on HTTP Notification or API Get Status.

Create separated web endpoint (notification url) to receive HTTP POST notification callback/webhook.
HTTP notification will be sent whenever transaction status is changed.
Example also available [here](examples/transaction_actions/notification_example.py)

```python
# Create Core API / Snap instance (both have shared `transactions` methods)
api_client = midtransclient.CoreApi(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
status_response = api_client.transactions.notification(mock_notification)

order_id = status_response['order_id']
transaction_status = status_response['transaction_status']
fraud_status = status_response['fraud_status']

print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {3}'.format(order_id,
    transaction_status,
    fraud_status))

# Sample transaction_status handling logic

if transaction_status == 'capture':
  if fraud_status == 'challenge':
    # TODO set transaction status on your databaase to 'challenge'
  else if fraud_status == 'accept':
    # TODO set transaction status on your databaase to 'success'
else if transaction_status == 'cancel' or
  transaction_status == 'deny' or
  transaction_status == 'expire':
  # TODO set transaction status on your databaase to 'failure'
else if transaction_status == 'pending':
  # TODO set transaction status on your databaase to 'pending' / waiting payment
```

### 2.4 Transaction Action
Also available as examples [here](examples/transaction_actions)
#### Get Status
```python
# get status of transaction that already recorded on midtrans (already `charge`-ed)
status_response = api_client.transactions.status('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Get Status B2B
```python
# get transaction status of VA b2b transaction
statusb2b_response = api_client.transactions.statusb2b('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Approve Transaction
```python
# approve a credit card transaction with `challenge` fraud status
approve_response = api_client.transactions.approve('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Deny Transaction
```python
# deny a credit card transaction with `challenge` fraud status
deny_response = api_client.transactions.deny('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Cancel Transaction
```python
# cancel a credit card transaction or pending transaction
cancel_response = api_client.transactions.cancel('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Expire Transaction
```python
# expire a pending transaction
expire_response = api_client.transactions.expire('YOUR_ORDER_ID OR TRANSACTION_ID')
```
#### Refund Transaction
```python
# refund a transaction (not all payment channel allow refund via API)
param = {
    "refund_key": "order1-ref1",
    "amount": 5000,
    "reason": "Item out of stock"
}
refund_response = api_client.transactions.refund('YOUR_ORDER_ID OR TRANSACTION_ID',param)
```

#### Refund Transaction with Direct Refund
```python
# refund a transaction (not all payment channel allow refund via API) with Direct Refund
param = {
    "refund_key": "order1-ref1",
    "amount": 5000,
    "reason": "Item out of stock"
}
refund_response = api_client.transactions.refundDirect('YOUR_ORDER_ID OR TRANSACTION_ID',param)
```

## 3. Handling Error / Exception
When using function that result in Midtrans API call e.g: `core.charge(...)` or `snap.create_transaction(...)`
there's a chance it may throw error (`MidtransAPIError` object), the error object will contains below properties that can be used as information to your error handling logic:
```python
err = None
try:
    transaction = snap.create_transaction(param)
except Exception as e:
    err = e
err.message
err.api_response_dict
err.http_status_code
err.raw_http_client_data
```
## 4. Advanced Usage

### Custom Http Headers

You can set custom headers via the value of this `<api-client-instance>.api_config.custom_headers` dict, e.g:
```python
# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# set custom HTTP header for every request from this instance
snap.api_config.custom_headers = {
    'my-custom-header':'my value',
    'x-override-notification':'https://example.org',
}
```

### Override/Append Http Notification Url
As [described in API docs](https://snap-docs.midtrans.com/#override-notification-url), merchant can opt to change or add custom notification urls on every transaction. It can be achieved by adding additional HTTP headers into charge request.

This can be achived by:
```python
# create instance of api client
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)
# set custom HTTP header that will be used by Midtrans API to override notification url:
snap.api_config.custom_headers = {
    'x-override-notification':'https://example.org',
}
```

or append notification:
```python
snap.api_config.custom_headers = {
    'x-append-notification':'https://example.org',
}
```

### Custom Http Proxy

You can set custom http(s) proxies via the value of this `<api-client-instance>.api_config.proxies` dict, e.g:

```python
# create instance of api client
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

snap.api_config.proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
```

Under the hood this API wrapper is using [Requests](https://github.com/requests/requests) as http client. You can further [learn about proxies on its documentation](https://requests.readthedocs.io/en/master/user/advanced/#proxies)

## Examples
Examples are available on [/examples](/examples) folder.
There are:
- [Core Api examples](/examples/core_api)
- [Subscription examples](/examples/subscription)
- [Tokenization examples](/examples/tokenization)
- [Snap examples](/examples/snap)
- [Flask App examples](/examples/flask_app) that implement Snap & Core Api

## Important Changes
### v1.3.0
- **Drop support for Python 2** (because Python 2 has reached its end of life), in favor of better compatibility with Python 3 and to prevent package unable to be properly installed on Windows OS env.

#### Get help

* [Midtrans Docs](https://docs.midtrans.com)
* [Midtrans Dashboard ](https://dashboard.midtrans.com/)
* [SNAP documentation](http://snap-docs.midtrans.com)
* [Core API documentation](http://api-docs.midtrans.com)
* Can't find answer you looking for? email to [support@midtrans.com](mailto:support@midtrans.com)
