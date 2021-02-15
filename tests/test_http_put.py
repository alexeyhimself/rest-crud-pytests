import pytest
import requests
import json

from conftest import T, SERVICE_URL, BEAR_DEFAULT_PARAMS

from conftest import VALID_BEAR_NAMES, VALID_BEAR_AGES, VALID_BEAR_TYPES
from conftest import INVALID_BEAR_NAMES, INVALID_BEAR_AGES, INVALID_BEAR_TYPES


#
#  Assist function.
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, updates one of bear specified params to a specified value. 
#  Then reads that bear and checks that specified parameter's value 
#  is the same.
#
def post_put_get_and_return_to_compare(valid_bear, param, value):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id = r1.text
  valid_param = {param: value}
  r2 = requests.put(SERVICE_URL + "/" + str(bear_id), data=json.dumps(valid_param), timeout=T)
  assert r2.status_code == 200
  assert r2.text == "OK"
  r3 = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r3.status_code == 200
  bear = json.loads(r3.text)
  assert bear.get(param) == value


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_name", VALID_BEAR_NAMES)
def test_update_bear_name_by_sending_only_that_valid_param(valid_bear, valid_bear_name):
  post_put_get_and_return_to_compare(valid_bear, "bear_name", valid_bear_name)


"""
update only 1 param by sending 1 param (for each param) (with valid/invalid data)
update only 1 param by sending all bear (for each param) (with valid/invalid data)
update not existing param
update bear_id by 1 param
update bear_id by whole bear
update bear_id by whole bear try overwrite

update bear to make it duplicate
update {}
update {not exists}
"""