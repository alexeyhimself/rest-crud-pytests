import pytest
import requests
import time
import json

from conftest import SERVICE_URL, T, T_MAX_FOR_LOAD_TEST, A_LOT


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.run_on_empty
def test_successfully_deletes_all_when_no_bears():
  r = requests.delete(SERVICE_URL, timeout=T)
  assert r.status_code == 200


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.smoke
def test_successfully_deletes_all_existing_bears(valid_bear, flush_with_data):
  flush_with_data(valid_bear)
  r1 = requests.delete(SERVICE_URL, timeout=T)
  assert r1.status_code == 200
  r2 = requests.get(SERVICE_URL, timeout=T)
  bears = json.loads(r2.text)
  assert bears == []


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.smoke
def test_successfully_deletes_existing_bear_by_id(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  bear_id = r1.text
  r2 = requests.delete(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r2.status_code == 200
  r3 = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r3.status_code == 200  # will be set to 404 when get will be fixed


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.smoke
def test_successfully_deletes_bear_by_id_that_does_not_exist(valid_bear):
  r1 = requests.post(SERVICE_URL, data=json.dumps(valid_bear), timeout=T)
  bear_id = r1.text
  r2 = requests.delete(SERVICE_URL + "/" + str(bear_id), timeout=T)
  assert r2.status_code == 200
  r3 = requests.delete(SERVICE_URL + "/" + str(bear_id), timeout=T)  # once again same id
  assert r2.status_code == 200


# @pytest.mark.d
@pytest.mark.performance
@pytest.mark.delete
@pytest.mark.slow
def test_successfully_deletes_all_bears_when_a_lot_bears_exist(valid_bear, flush_with_data):
  flush_with_data(valid_bear, how_many_bears=A_LOT)
  time_start = time.monotonic()
  r = requests.delete(SERVICE_URL, timeout=T_MAX_FOR_LOAD_TEST)
  time_end = time.monotonic()
  assert r.status_code == 200
  assert time_end - time_start < T_MAX_FOR_LOAD_TEST
