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
        api_url = self.api_config.get_core_api_base_url()+'/charge'

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
        api_url = self.api_config.get_core_api_base_url()+'/capture'

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
        api_url = self.api_config.get_core_api_base_url()+'/card/register'

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
        api_url = self.api_config.get_core_api_base_url()+'/token'

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
        api_url = self.api_config.get_core_api_base_url()+'/point_inquiry/'+token_id

        response_dict, response_object = self.http_client.request(
            'get',
            self.api_config.server_key,
            api_url,
            dict(),
            self.api_config.custom_headers,
            self.api_config.proxies)

        return response_dict