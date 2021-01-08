import midtransclient
# initialize snap client object
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOUR_SERVER_KEY',
    client_key='YOUR_CLIENT_KEY'
)

# Alternative way to initialize snap client object:
# snap = midtransclient.Snap()
# snap.api_config.set(
#     is_production=False,
#     server_key='YOUR_SERVER_KEY',
#     client_key='YOUR_CLIENT_KEY'
# )

# Another alternative way to initialize snap client object:
# snap = midtransclient.Snap()
# snap.api_config.is_production=False
# snap.api_config.server_key='YOUR_SERVER_KEY'
# snap.api_config.client_key='YOUR_CLIENT_KEY'

# prepare SNAP API parameter ( refer to: https://snap-docs.midtrans.com ) this is full parameter including optionals parameter.
param = {
    "transaction_details": {
        "order_id": "test-transaction-1234",
        "gross_amount": 10000
    },
    "item_details": [{
        "id": "ITEM1",
        "price": 10000,
        "quantity": 1,
        "name": "Midtrans Bear",
        "brand": "Midtrans",
        "category": "Toys",
        "merchant_name": "Midtrans"
    }],
    "customer_details": {
        "first_name": "John",
        "last_name": "Watson",
        "email": "test@example.com",
        "phone": "+628123456",
        "billing_address": {
            "first_name": "John",
            "last_name": "Watson",
            "email": "test@example.com",
            "phone": "081 2233 44-55",
            "address": "Sudirman",
            "city": "Jakarta",
            "postal_code": "12190",
            "country_code": "IDN"
        },
        "shipping_address": {
            "first_name": "John",
            "last_name": "Watson",
            "email": "test@example.com",
            "phone": "0 8128-75 7-9338",
            "address": "Sudirman",
            "city": "Jakarta",
            "postal_code": "12190",
            "country_code": "IDN"
        }
    },
    "enabled_payments": ["credit_card", "mandiri_clickpay", "cimb_clicks","bca_klikbca", "bca_klikpay", "bri_epay", "echannel", "indosat_dompetku","mandiri_ecash", "permata_va", "bca_va", "bni_va", "other_va", "gopay","kioson", "indomaret", "gci", "danamon_online"],
    "credit_card": {
        "secure": True,
        "bank": "bca",
        "installment": {
            "required": False,
            "terms": {
                "bni": [3, 6, 12],
                "mandiri": [3, 6, 12],
                "cimb": [3],
                "bca": [3, 6, 12],
                "offline": [6, 12]
            }
        },
        "whitelist_bins": [
            "48111111",
            "41111111"
        ]
    },
    "bca_va": {
        "va_number": "12345678911",
        "free_text": {
            "inquiry": [
                {
                    "en": "text in English",
                    "id": "text in Bahasa Indonesia"
                }
            ],
            "payment": [
                {
                    "en": "text in English",
                    "id": "text in Bahasa Indonesia"
                }
            ]
        }
    },
    "bni_va": {
        "va_number": "12345678"
    },
    "permata_va": {
        "va_number": "1234567890",
        "recipient_name": "SUDARSONO"
    },
    "callbacks": {
        "finish": "https://demo.midtrans.com"
    },
    "expiry": {
        "start_time": "2025-12-20 18:11:08 +0700",
        "unit": "minute",
        "duration": 9000
    },
    "custom_field1": "custom field 1 content",
    "custom_field2": "custom field 2 content",
    "custom_field3": "custom field 3 content"
}

# create transaction
transaction = snap.create_transaction(param)

# transaction token
transaction_token = transaction['token']
print('transaction_token:')
print(transaction_token)

# transaction redirect url
transaction_url = transaction['redirect_url']
print('transaction_url:')
print(transaction_url)

# alternative way to create transaction_token:
transaction_token = snap.create_transaction_token(param)
print('transaction_token:')
print(transaction_token)

# alternative way to create transaction_url:
transaction_url = snap.create_transaction_redirect_url(param)
print('transaction_url:')
print(transaction_url)
