import pytest
import requests
import json

from conftest import SERVICE_URL, T, BEAR_DEFAULT_PARAMS
from conftest import VALID_BEAR_NAMES, VALID_BEAR_AGES, VALID_BEAR_TYPES
from conftest import INVALID_BEAR_NAMES, INVALID_BEAR_AGES, INVALID_BEAR_TYPES


# @pytest.mark.d
@pytest.mark.smoke
def test_successfully_creates_valid_bear(valid_bear):
  r = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r.status_code == 200
  assert r.text.isdigit() == True


# @pytest.mark.d
def test_successfully_creates_duplicate_valid_bear(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  r2 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  assert r2.text.isdigit() == True


#
#  Assist function for valid data verification.
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, reads that bear and checks that specified parameter's value 
#  is the same.
#
def post_get_and_compare(valid_bear, param, value):
  valid_bear[param] = value
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  valid_bear_id = r1.text
  assert r1.text.isdigit() == True
  r2 = requests.get(SERVICE_URL + "/" + str(valid_bear_id), timeout=T)
  assert r2.status_code == 200
  bear = json.loads(r2.text)
  assert isinstance(bear, dict) == True
  assert bear.get(param) == valid_bear.get(param)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_type", VALID_BEAR_TYPES)
def test_successfully_creates_bear_with_valid_bear_type(valid_bear, valid_bear_type):
  post_get_and_compare(valid_bear, "bear_type", valid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_name", VALID_BEAR_NAMES)
def test_successfully_creates_bear_with_valid_bear_name(valid_bear, valid_bear_name):
  post_get_and_compare(valid_bear, "bear_name", valid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_age", VALID_BEAR_AGES)
def test_successfully_creates_bear_with_valid_bear_age(valid_bear, valid_bear_age):
  post_get_and_compare(valid_bear, "bear_age", valid_bear_age)


#
#  Assist function for invalid data verification.
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Tries to create a bear and checks that it got HTTP 400 response
#
def post_and_get_400(valid_bear, param, value):
  valid_bear[param] = value
  r = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_type", INVALID_BEAR_TYPES)
def test_fails_to_create_bear_with_invalid_bear_type(valid_bear, invalid_bear_type):
  post_and_get_400(valid_bear, "bear_type", invalid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_name", INVALID_BEAR_NAMES)
def test_fails_to_create_bear_with_invalid_bear_name(valid_bear, invalid_bear_name):
  post_and_get_400(valid_bear, "bear_name", invalid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_age", INVALID_BEAR_AGES)
def test_fails_to_create_bear_with_invalid_bear_age(valid_bear, invalid_bear_age):
  post_and_get_400(valid_bear, "bear_age", invalid_bear_age)


# @pytest.mark.d
@pytest.mark.parametrize("default_param", BEAR_DEFAULT_PARAMS)
def test_fails_to_create_bear_without_any_default_param(valid_bear, default_param):
  valid_bear.pop(default_param)
  r = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_create_bear_without_any_params():
  r = requests.post(SERVICE_URL, data="{}", timeout=T)
  assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_create_bear_with_only_unknown_param():
  unknown_param = {"unknown": "param"}
  r = requests.post(SERVICE_URL, data=json.dumps(unknown_param), timeout=T)
  assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_successfully_creates_bear_with_valid_params_and_unknown_param(valid_bear):
  valid_bear["unknown"] = "param"
  r = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r.status_code == 200
  assert r.text.isdigit() == True
