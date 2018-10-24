import pytest
from .context import midtransclient
from pprint import pprint

def test_midtransclient_module():
	attributes = dir(midtransclient)
	assert 'Snap' in attributes
	assert 'CoreApi' in attributes