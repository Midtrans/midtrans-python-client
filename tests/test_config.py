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
    # assert repr(apiconfig) == '<ApiConfig(False,sk-abc,ck-123,{})>'

def test_api_config_class_with_custom_headers():
    apiconfig = ApiConfig(is_production=False,
        server_key='sk-abc',
        client_key='ck-123',
        custom_headers={'X-Override-Notification':'https://example.org'})
    assert apiconfig.is_production == False
    assert apiconfig.server_key == 'sk-abc'
    assert apiconfig.client_key == 'ck-123'
    assert 'sk-abc' in repr(apiconfig)
    assert 'ck-123' in repr(apiconfig)
    assert 'X-Override-Notification' in repr(apiconfig)

def test_api_config_class_with_proxies():
    apiconfig = ApiConfig(is_production=False,
        server_key='sk-abc',
        client_key='ck-123',
        custom_headers=dict(),
        proxies={
          'http': 'http://example.org:3128',
          'https': 'http://example.org:1080',
        })
    assert apiconfig.is_production == False
    assert apiconfig.server_key == 'sk-abc'
    assert apiconfig.client_key == 'ck-123'
    assert 'sk-abc' in repr(apiconfig)
    assert 'ck-123' in repr(apiconfig)
    assert 'example.org:1080' in repr(apiconfig)