import pytest
from .context import ApiConfig
from pprint import pprint

def test_api_config_class():
	apiconfig = ApiConfig(is_production=False,
        server_key='sk-abc',
        client_key='ck-123')
	assert apiconfig.is_production == False
	assert apiconfig.server_key == 'sk-abc'
	assert apiconfig.client_key == 'ck-123'
	assert repr(apiconfig) == '<ApiConfig(False,sk-abc,ck-123)>'