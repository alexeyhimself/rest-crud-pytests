import pytest
import requests
import json

from conftest import T, SERVICE_URL

from conftest import VALID_BEAR_NAMES, VALID_BEAR_AGES, VALID_BEAR_TYPES
from conftest import INVALID_BEAR_NAMES, INVALID_BEAR_AGES, INVALID_BEAR_TYPES


#
#  Assist function for valid data verification (part).
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, updates one of bear specified params to a specified value
#  by sending only that particular change. Then reads that bear and checks that 
#  specified parameter's value is as updated.
#
def post_put_part_get_and_compare(valid_bear, param, value):
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
def test_successfully_updates_bear_name_by_sending_only_that_valid_param(valid_bear, valid_bear_name):
  post_put_part_get_and_compare(valid_bear, "bear_name", valid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_type", VALID_BEAR_TYPES)
def test_successfully_updates_bear_type_by_sending_only_that_valid_param(valid_bear, valid_bear_type):
  post_put_part_get_and_compare(valid_bear, "bear_type", valid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_age", VALID_BEAR_AGES)
def test_successfully_updates_bear_age_by_sending_only_that_valid_param(valid_bear, valid_bear_age):
  post_put_part_get_and_compare(valid_bear, "bear_age", valid_bear_age)


#
#  Assist function for invalid data verification (part).
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, tries to update one of bear specified params to a specified value
#  by sending only that particular change and checks that it got HTTP 400 response.
#
def post_put_part_and_get_400(valid_bear, param, value):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id = r1.text
  valid_param = {param: value}
  r2 = requests.put(SERVICE_URL + "/" + str(bear_id), data=json.dumps(valid_param), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_name", INVALID_BEAR_NAMES)
def test_fails_to_update_bear_name_by_sending_only_that_invalid_param(valid_bear, invalid_bear_name):
  post_put_part_and_get_400(valid_bear, "bear_name", invalid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_type", INVALID_BEAR_TYPES)
def test_fails_to_update_bear_type_by_sending_only_that_invalid_param(valid_bear, invalid_bear_type):
  post_put_part_and_get_400(valid_bear, "bear_type", invalid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_age", INVALID_BEAR_AGES)
def test_fails_to_update_bear_age_by_sending_only_that_invalid_param(valid_bear, invalid_bear_age):
  post_put_part_and_get_400(valid_bear, "bear_age", invalid_bear_age)


# @pytest.mark.d
def test_fails_to_update_bear_unknown_parameter_sending_only_that_invalid_param(valid_bear):
  post_put_part_and_get_400(valid_bear, "unknown", "parameter")


# @pytest.mark.d
def test_fails_to_update_bear_id_to_free_id_by_sending_only_that_param(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  bear_id2 = r2.text
  r3 = requests.delete(SERVICE_URL + "/" + str(bear_id1), timeout=T)  # make bear_id1 free
  assert r3.status_code == 200
  broken_param = {"bear_id": bear_id1}
  r4 = requests.put(SERVICE_URL + "/" + str(bear_id2), data=json.dumps(broken_param), timeout=T)
  assert r2.status_code == 400


# @pytest.mark.d
def test_fails_to_update_bear_id_to_already_by_used_id_sending_only_that_param(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  bear_id2 = r2.text
  broken_param = {"bear_id": bear_id1}
  r4 = requests.put(SERVICE_URL + "/" + str(bear_id2), data=json.dumps(broken_param), timeout=T)
  assert r2.status_code == 400

#
#  Assist function for valid data verification (whole).
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, updates one of bear specified params to a specified value
#  by sending whole new bear as an update. Then reads that bear and checks that 
#  specified parameter's value is as updated.
#
def post_put_whole_get_and_compare(valid_bear, param, value):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id = r1.text
  valid_bear[param] = value
  r2 = requests.put(SERVICE_URL + "/" + str(bear_id), data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  assert r2.text == "OK"
  r3 = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r3.status_code == 200
  bear = json.loads(r3.text)
  assert bear.get(param) == value


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_name", VALID_BEAR_NAMES)
def test_successfully_updates_bear_name_by_sending_whole_valid_updated_bear(valid_bear, valid_bear_name):
  post_put_whole_get_and_compare(valid_bear, "bear_name", valid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_type", VALID_BEAR_TYPES)
def test_successfully_updates_bear_type_by_sending_whole_valid_updated_bear(valid_bear, valid_bear_type):
  post_put_whole_get_and_compare(valid_bear, "bear_type", valid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("valid_bear_age", VALID_BEAR_AGES)
def test_successfully_updates_bear_age_by_sending_whole_valid_updated_bear(valid_bear, valid_bear_age):
  post_put_whole_get_and_compare(valid_bear, "bear_age", valid_bear_age)


#
#  Assist function for invalid data verification (whole).
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, tries to update one of bear specified params to a specified value
#  by sending whole new bear as an update and checks that it got HTTP 400 response.
#
def post_put_whole_and_get_400(valid_bear, param, value):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id = r1.text
  valid_bear[param] = value
  r2 = requests.put(SERVICE_URL + "/" + str(bear_id), data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_name", INVALID_BEAR_NAMES)
def test_fails_to_update_bear_name_by_sending_whole_invalid_updated_bear(valid_bear, invalid_bear_name):
  post_put_whole_and_get_400(valid_bear, "bear_name", invalid_bear_name)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_type", INVALID_BEAR_TYPES)
def test_fails_to_update_bear_type_by_sending_whole_invalid_updated_bear(valid_bear, invalid_bear_type):
  post_put_whole_and_get_400(valid_bear, "bear_type", invalid_bear_type)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_bear_age", INVALID_BEAR_AGES)
def test_fails_to_update_bear_age_by_sending_whole_invalid_updated_bear(valid_bear, invalid_bear_age):
  post_put_whole_and_get_400(valid_bear, "bear_age", invalid_bear_age)


# @pytest.mark.d
def test_fails_to_update_bear_id_to_free_id_by_sending_whole_invalid_updated_bear(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  bear_id2 = r2.text
  r3 = requests.delete(SERVICE_URL + "/" + str(bear_id1), timeout=T)  # make bear_id1 free
  assert r3.status_code == 200
  valid_bear["bear_id"] = bear_id1  # making bear id invalid
  invalid_bear = valid_bear
  r4 = requests.put(SERVICE_URL + "/" + str(bear_id2), data=json.dumps(invalid_bear), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_update_bear_id_to_already_by_used_id_sending_whole_invalid_updated_bear(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r2.status_code == 200
  bear_id2 = r2.text
  valid_bear["bear_id"] = bear_id1  # making bear id invalid
  invalid_bear = valid_bear
  r4 = requests.put(SERVICE_URL + "/" + str(bear_id2), data=json.dumps(invalid_bear), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_update_bear_with_empty_dict(valid_bear, cleanup):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps({}), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_update_bear_with_dict_with_unknown_parameters(valid_bear, cleanup):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  assert r1.status_code == 200
  bear_id1 = r1.text
  r2 = requests.post(SERVICE_URL, data=json.dumps({"unknown": "param"}), timeout=T)
  assert r2.status_code == 400  # must be HTTP 400 Bad Request

###

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