from .config import ApiConfig
from .http_client import HttpClient

class Tokenization:
    """
    Link the customer's account to be used for payments using specific payment channel
    (more params detail refer to: https://api-docs.midtrans.com/#gopay-tokenization)
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

    def link_account(self,parameters=dict()):
        """
        Trigger `/v2/pay/account` API call to Core API
        Link the customer account to be used for specific payment channels.
        :param parameters: dictionary of Core API JSON body as parameter, will be converted to JSON
        (more params detail refer to: https://api-docs.midtrans.com/#create-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v2/pay/account'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            parameters,
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def get_account(self,account_id):
        """
        Trigger `/v2/pay/account/<account_id>` API call to Core API
        Retrieve the payment account details of a customer using the account_id
        (more params detail refer to: https://api-docs.midtrans.com/#get-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v2/pay/account/'+account_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict

    def unlink_account(self,account_id):
        """
        Trigger `/v2/pay/account/<account_id>/unbind` API call to Core API
        To remove the linked customer account
        (more params detail refer to: https://api-docs.midtrans.com/#unbind-pay-account)

        :return: Dictionary from JSON decoded response
        """
        api_url = self.api_config.get_base_url()+'/v2/pay/account/'+account_id+'/unbind'

        response_dict, response_object = self.http_client.request(
            'post',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict
