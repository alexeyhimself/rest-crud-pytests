import pytest
import requests
import json
import time
import sys

from conftest import SERVICE_URL, T, T_MAX_FOR_LOAD_TEST, A_LOT
from conftest import INVALID_IDS


# @pytest.mark.d
@pytest.mark.run_on_empty
def test_read_all_bears_when_bears_not_exist():
  r = requests.get(SERVICE_URL, timeout=T)
  assert r.status_code == 200
  bears = json.loads(r.text)
  assert bears == []


# @pytest.mark.d
@pytest.mark.smoke
def test_read_all_bears_when_bears_exist(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  r2 = requests.get(SERVICE_URL, timeout=T)
  assert r2.status_code == 200
  bears = json.loads(r2.text)
  assert isinstance(bears, list) == True
  assert len(bears) >= 1


# @pytest.mark.d
@pytest.mark.slow
@pytest.mark.performance
def test_read_all_bears_when_a_lot_bears_exist(valid_bear, flush_with_data):
  flush_with_data(valid_bear, how_many_bears=A_LOT)
  time_start = time.monotonic()
  r = requests.get(SERVICE_URL, timeout=T_MAX_FOR_LOAD_TEST)
  time_end = time.monotonic()
  assert r.status_code == 200
  bears = json.loads(r.text)
  assert isinstance(bears, list) == True
  assert len(bears) >= A_LOT
  assert time_end - time_start < T_MAX_FOR_LOAD_TEST


# @pytest.mark.d
@pytest.mark.parametrize("invalid_id", INVALID_IDS)
def test_read_bear_by_invalid_id_returns_http_404(invalid_id):
  r = requests.get(SERVICE_URL + "/" + str(invalid_id), timeout=T)
  assert r.status_code == 404  # why returns HTTP 200, not 400 bad request or 404 not found?
                               # if HTTP 200, then why returns word EMPTY rather than []?
                               # considering this 200 as a bug for HTTP REST


# @pytest.mark.d
def test_read_bear_by_large_out_of_range_id():
  r = requests.get(SERVICE_URL + "/" + str(sys.maxsize + 1), timeout=T)
  assert r.status_code == 404


# @pytest.mark.d
def test_read_bear_by_valid_id_that_not_exist():
  r = requests.get(SERVICE_URL + "/" + str(sys.maxsize - 1), timeout=T)
  assert r.status_code == 404


# @pytest.mark.d
@pytest.mark.smoke
def test_read_existing_bear_by_id(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  bear_id = r1.text
  r2 = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r2.status_code == 200
  bear = json.loads(r2.text)
  assert isinstance(bear, dict) == True


# @pytest.mark.d
def test_read_json_is_the_same_as_post_json(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  bear_id = r1.text
  r2 = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r2.status_code == 200
  bear = json.loads(r2.text)
  assert isinstance(bear, dict) == True
  valid_bear["bear_id"] = bear_id
  assert bear == valid_bear