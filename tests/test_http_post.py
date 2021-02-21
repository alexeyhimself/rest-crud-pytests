"""

  Tests in this file

  Positive:
    * Create valid bear works: test_successfully_creates_valid_bear
    * Create duplicate bear works: test_successfully_creates_duplicate_valid_bear
    * Create bear with each valid bear_type works: test_successfully_creates_bear_with_valid_bear_type
    * Create bear with each valid bear_name works: test_successfully_creates_bear_with_valid_bear_name
    * Create bear with each valid bear_age works: test_successfully_creates_bear_with_valid_bear_age
    * Create valid bear with unknown parameter works: test_successfully_creates_bear_with_valid_params_and_unknown_param

  Conditionally-negative:
    * Create bear with various invalid bear_types does not work: test_fails_to_create_bear_with_invalid_bear_type
    * Create bear with various invalid bear_names does not work: test_fails_to_create_bear_with_invalid_bear_name
    * Create bear with various invalid bear_ages does not work: test_fails_to_create_bear_with_invalid_bear_age

    * Create bear without any one of default parameters does not work: test_fails_to_create_bear_without_any_default_param
    * Create bear with invalid payload format does not work: test_fails_to_create_bear_with_broken_format_data_param
    * Create bear with valid format but invalid set does not work: test_fails_to_create_bear_with_only_unknown_param

"""

import pytest
import requests
import json

from conftest import SERVICE_URL, T, BEAR_DEFAULT_PARAMS
from conftest import VALID_BEAR_NAMES, VALID_BEAR_AGES, VALID_BEAR_TYPES
from conftest import INVALID_BEAR_NAMES, INVALID_BEAR_AGES, INVALID_BEAR_TYPES
from conftest import INVALID_DATASET

from conftest import BearsDB


class BearsDBExtended(BearsDB):
  def create_bear_bad_request(self, bear):
    r = requests.post(SERVICE_URL, data=json.dumps(bear), timeout=T)
    assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
@pytest.mark.smoke
def test_successfully_creates_valid_bear(valid_bear):
  bears_db = BearsDB()
  bears_db.create_bear(valid_bear)


# @pytest.mark.d
def test_successfully_creates_duplicate_valid_bear(valid_bear):
  bears_db = BearsDB()
  bears_db.create_bear(valid_bear)
  bears_db.create_bear(valid_bear)


#
#  Assist function for valid data verification.
# 
#  Gets valid_bear dict and changes one of it's specified params to specified value.
#  Creates a bear, reads that bear and checks that specified parameter's value 
#  is the same.
#
def post_get_and_compare(valid_bear, param, value):
  valid_bear[param] = value
  bears_db = BearsDB()
  bear_id = bears_db.create_bear(valid_bear)
  bear = bears_db.read_bear(bear_id)
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
  bears_db = BearsDBExtended()
  bears_db.create_bear_bad_request(valid_bear)


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
  bears_db = BearsDBExtended()
  bears_db.create_bear_bad_request(valid_bear)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_data", INVALID_DATASET)
def test_fails_to_create_bear_with_broken_format_data_param(invalid_data):
  r = requests.post(SERVICE_URL, data=invalid_data, timeout=T)
  assert r.status_code == 400  # must be HTTP 400 Bad Request


# @pytest.mark.d
def test_fails_to_create_bear_with_only_unknown_param():
  unknown_param = {"unknown": "param"}
  bears_db = BearsDBExtended()
  bears_db.create_bear_bad_request(unknown_param)


# @pytest.mark.d
def test_successfully_creates_bear_with_valid_params_and_unknown_param(valid_bear):
  valid_bear["unknown"] = "param"
  bears_db = BearsDB()
  bears_db.create_bear(valid_bear)
