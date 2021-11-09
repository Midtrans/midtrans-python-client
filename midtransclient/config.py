class ApiConfig:
    """
    Config Object that used to store is_production, server_key, client_key.
    And also API base urls.
    note: client_key is not necessarily required for API call.
    """
    CORE_SANDBOX_BASE_URL = 'https://api.sandbox.midtrans.com';
    CORE_PRODUCTION_BASE_URL = 'https://api.midtrans.com';
    SNAP_SANDBOX_BASE_URL = 'https://app.sandbox.midtrans.com/snap/v1';
    SNAP_PRODUCTION_BASE_URL = 'https://app.midtrans.com/snap/v1';

    def __init__(self, 
            is_production=False,
            server_key='',
            client_key='',
            custom_headers=dict(),
            proxies=dict()):
        self.is_production = is_production
        self.server_key = server_key
        self.client_key = client_key
        self.custom_headers = custom_headers
        self.proxies = proxies

    def get_core_api_base_url(self):
        if self.is_production: 
            return self.CORE_PRODUCTION_BASE_URL
        return self.CORE_SANDBOX_BASE_URL 

    def get_snap_base_url(self):
        if self.is_production: 
            return self.SNAP_PRODUCTION_BASE_URL
        return self.SNAP_SANDBOX_BASE_URL 

    # properties setter
    def set(self,
            is_production=None,
            server_key=None,
            client_key=None):
        if is_production is not None:
            self.is_production = is_production
        if server_key is not None:
            self.server_key = server_key
        if client_key is not None:
            self.client_key = client_key

    @property
    def server_key(self):
        return self.__server_key
    
    @server_key.setter
    def server_key(self, new_value):
        self.__server_key = new_value

    @property
    def client_key(self):
        return self.__client_key
    
    @client_key.setter
    def client_key(self, new_value):
        self.__client_key = new_value

    @property
    def custom_headers(self):
        return self.__custom_headers

    @custom_headers.setter
    def custom_headers(self, new_value):
        self.__custom_headers = new_value

    @property
    def proxies(self):
        return self.__proxies

    @proxies.setter
    def proxies(self, new_value):
        self.__proxies = new_value

    def __repr__(self):
        return ("<ApiConfig({0},{1},{2},{3},{4})>".format(self.is_production,
            self.server_key,
            self.client_key,
            self.custom_headers,
            self.proxies))