from .config import ApiConfig
from .http_client import HttpClient
from .transactions import Transactions

class CoreApi:
    """
    CoreApi object used to do request to Midtrans Core API
    """

    def __init__(self, 
            is_production=False,
            server_key='',
            client_key='',
            custom_headers=dict(),
            proxies=dict()):

        self.api_config = ApiConfig(is_production,server_key,client_key,custom_headers,proxies)
        self.http_client = HttpClient()
        self.transactions = Transactions(self)

    @property
    def api_config(self):
        return self.__api_config

    @api_config.setter
    def api_config(self, new_value):
        self.__api_config = new_value

    def charge(self,parameters=dict()):
        """
        Trigger `/charge` API call to Core API
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/charge'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters)

        return response_dict

    def capture(self,parameters=dict()):
        """
        Trigger `/capture` API call to Core API
        Capture is only used for pre-authorize transaction only
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/capture'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def card_register(self,parameters=dict()):
        """
        Trigger `/card/register` API call to Core API
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/card/register'

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def card_token(self,parameters=dict()):
        """
        Trigger `/token` API call to Core API
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/token'

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)
        
        return response_dict

    def card_point_inquiry(self,token_id):
        """
        Trigger `/point_inquiry/<token-id>` API call to Core API
        :param token_id: token id of credit card
        (more params detail refer to: https://api-docs.midtrans.com)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/point_inquiry/'+token_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def create_subscription(self,parameters=dict()):
        """
        Trigger `/v1/subscriptions` API call to Core API
        Create a subscription transaction by sending all the details required to create a transaction
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com/#create-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v1/subscriptions'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def get_subscription(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>` API call to Core API
        Retrieve the subscription details of a customer using the subscription_id
        (more params detail refer to: https://api-docs.midtrans.com/#get-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v1/subscriptions/'+subscription_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def disable_subscription(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>/disable` API call to Core API
        Disable the customer's subscription. The customer will not be charged in the future for this subscription
        (more params detail refer to: https://api-docs.midtrans.com/#disable-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v1/subscriptions/'+subscription_id+'/disable'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def enable_subscription(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>/enable` API call to Core API
        Enable the customer's subscription
        (more params detail refer to: https://api-docs.midtrans.com/#enable-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v1/subscriptions/'+subscription_id+'/enable'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)
        
        return response_dict

    def update_subscription(self,subscription_id,parameters=dict()):
        """
        Trigger `/v1/subscriptions/<subscription_id>` API call to Core API
        Update existing subscription details
        (more params detail refer to: https://api-docs.midtrans.com/#update-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v1/subscriptions/'+subscription_id

        response_dict, response_object = self.http_client.request(
            'patch',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict
        
    def link_payment_account(self,parameters=dict()):
        """
        Trigger `/v2/pay/account` API call to Core API
        Link the customer account to be used for specific payment channels.
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com/#create-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/pay/account'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def get_payment_account(self,account_id):
        """
        Trigger `/v2/pay/account/<account_id>` API call to Core API
        Retrieve the payment account details of a customer using the account_id
        (more params detail refer to: https://api-docs.midtrans.com/#get-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/pay/account/'+account_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def unlink_payment_account(self,account_id):
        """
        Trigger `/v2/pay/account/<account_id>/unbind` API call to Core API
        To remove the linked customer account
        (more params detail refer to: https://api-docs.midtrans.com/#unbind-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_core_api_base_url()+'/v2/pay/account/'+account_id+'/unbind'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict
