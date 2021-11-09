# This is just for very basic implementation reference, in production, you should validate the incoming requests and implement your backend more securely.
import midtransclient
import datetime

# Initialize core api client object
# You can find it in Merchant Portal -> Settings -> Access keys
core_api = midtransclient.CoreApi(
    is_production=False,
    server_key='SB-Mid-server-1isH_dlGSg6uy.I7NpeNK53i',
    client_key='SB-Mid-client-yrY4WjUNOnhOyIIH'
)

# prepare parameter ( refer to: https://api-docs.midtrans.com/#create-pay-account )
param = {
  "payment_type": "gopay",
  "gopay_partner": {
    "phone_number": "81234567891",
    "country_code": "62",
    "redirect_url": "https://midtrans.com"
  }
}

# link payment account
link_payment_account = core_api.link_payment_account(param)
print('link_payment_account_response:')
print(link_payment_account)

# link_payment_account_response is dictionary representation of API JSON response
# sample:
# {
#     "status_code": "201",
#     "payment_type": "gopay",
#     "account_id": "6e902848-c4c3-4f40-abe6-109e8749df21",
#     "account_status": "PENDING",
#     "actions": [
#         {
#             "name": "activation-deeplink",
#             "method": "GET",
#             "url": "https://api-v2.sandbox.midtrans.com/v2/pay/account/gpar_2b78cfea-2afa-49b3-86d5-3866626ce015/link"
#         },
#         {
#             "name": "activation-link-url",
#             "method": "GET",
#             "url": "https://api-v2.sandbox.midtrans.com/v2/pay/account/gpar_2b78cfea-2afa-49b3-86d5-3866626ce015/link"
#         },
#         {
#             "name": "activation-link-app",
#             "method": "GET",
#             "url": "https://simulator-v2.sandbox.midtrans.com/gopay/partner/web/otp?id=e4514b08-cc16-486e-9e4a-d8d8dd0bfe49"
#         }
#     ],
#     "metadata": {
#         "reference_id": "48b854c9-cc65-4af2-a3f0-38ae81798512"
#     }
# }
# for the first link, the account status is PENDING, you must activate it by accessing one of the URLs on the actions object

active_account_id = "6975fc98-8d44-490d-b50a-28d2810d6856"
# get payment account by account_id
get_payment_account = core_api.get_payment_account(active_account_id)
print('get_payment_account_response:')
print(get_payment_account)
# sample
# {
#     "status_code": "200",
#     "payment_type": "gopay",
#     "account_id": "6975fc98-8d44-490d-b50a-28d2810d6856",
#     "account_status": "ENABLED",
#     "metadata": {
#         "payment_options": [
#             {
#                 "name": "PAY_LATER",
#                 "active": true,
#                 "balance": {
#                     "value": "4649999.00",
#                     "currency": "IDR"
#                 },
#                 "metadata": {},
#                 "token": "04ed77b7-5ad5-4ba5-b631-d72aa369c2f7"
#             },
#             {
#                 "name": "GOPAY_WALLET",
#                 "active": true,
#                 "balance": {
#                     "value": "6100000.00",
#                     "currency": "IDR"
#                 },
#                 "metadata": {},
#                 "token": "8035816f-462e-4fa1-a5ef-c30bf71e2ee6"
#             }
#         ]
#     }
# }

# request charge 
params = {
  "payment_type": "gopay",
  "gopay": {
    "account_id": get_payment_account['account_id'],
    "payment_option_token": get_payment_account['metadata']['payment_options'][0]['token'],
    "callback_url": "https://midtrans.com"
  },
  "transaction_details": {
    "gross_amount": 100000,
    "order_id": "GOPAY-LINK-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  }
}
charge = core_api.charge(params)
print('charge_response:')
print(charge)


# unlink payment account by account_id
# when account status still PENDING, you will get status code 412
# sample response
# {
#     "status_code": "412",
#     "status_message": "Account status cannot be updated.",
#     "id": "19eda9e4-37c9-4bfd-abb2-c60bb3a91084"
# }
try:
    unlink_payment_account = core_api.unlink_payment_account(link_payment_account['account_id'])
    print('unlink_response:')
    print(unlink_payment_account)
except Exception as e:
    print('unlink_failure_response:')
    print(e)
