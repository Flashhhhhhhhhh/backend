import sys
sys.path.insert(0, 'src')

import CsvInterpreter

def test_parse_file():
    assert CsvInterpreter.parse_file("dataTemp.csv")

import json
import pytest
import requests
import server

@pytest.fixture
def app():
    app = create_app()
    return app

def client(request):
    test_client = app.test_client()
    return test_client

url = 'http://127.0.0.1:5002'

def test_index_page():
    r = requests.get(url+'/')
    assert r.status_code == 200 
