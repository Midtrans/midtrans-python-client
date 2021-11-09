from .config import ApiConfig
from .http_client import HttpClient

class Subscription:
    """
    Subscription API is intended for recurring transactions - transactions that deduct customer's funds at a pre-defined time interval.
    (more params detail refer to: https://api-docs.midtrans.com/#subscription-api)
    """

    def __init__(self, 
            is_production=False,
            server_key='',
            client_key='',
            custom_headers=dict(),
            proxies=dict()):

        self.api_config = ApiConfig(is_production,server_key,client_key,custom_headers,proxies)
        self.http_client = HttpClient()

    @property
    def api_config(self):
        return self.__api_config

    @api_config.setter
    def api_config(self, new_value):
        self.__api_config = new_value

    def create(self,parameters=dict()):
        """
        Trigger `/v1/subscriptions` API call to Core API
        Create a subscription transaction by sending all the details required to create a transaction
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com/#create-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v1/subscriptions'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def get(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>` API call to Core API
        Retrieve the subscription details of a customer using the subscription_id
        (more params detail refer to: https://api-docs.midtrans.com/#get-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v1/subscriptions/'+subscription_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def disable(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>/disable` API call to Core API
        Disable the customer's subscription. The customer will not be charged in the future for this subscription
        (more params detail refer to: https://api-docs.midtrans.com/#disable-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v1/subscriptions/'+subscription_id+'/disable'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def enable(self,subscription_id):
        """
        Trigger `/v1/subscriptions/<subscription_id>/enable` API call to Core API
        Enable the customer's subscription
        (more params detail refer to: https://api-docs.midtrans.com/#enable-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v1/subscriptions/'+subscription_id+'/enable'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)
        
        return response_dict

    def update(self,subscription_id,parameters=dict()):
        """
        Trigger `/v1/subscriptions/<subscription_id>` API call to Core API
        Update existing subscription details
        (more params detail refer to: https://api-docs.midtrans.com/#update-subscription)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v1/subscriptions/'+subscription_id

        response_dict, response_object = self.http_client.request(
            'patch',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict
        