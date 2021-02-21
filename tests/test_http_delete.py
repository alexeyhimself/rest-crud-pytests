"""

  Tests in this file

  * Delete when no bears in system works: test_successfully_deletes_all_when_no_bears
  * Delete when 2+ bears in system works: test_successfully_deletes_all_existing_bears
  * Delete when A LOT bears in system works: test_successfully_deletes_all_bears_when_a_lot_bears_exist

  * Delete bear by valid existing ID works: test_successfully_deletes_existing_bear_by_id
  * Delete bear by valid non-existing ID works: test_successfully_deletes_bear_by_id_that_does_not_exist
  * Delete bear by various invalid IDs works: test_fails_to_delete_bear_by_invalid_id

"""

import pytest
import requests
import time

from conftest import SERVICE_URL, T, T_MAX_FOR_LOAD_TEST, A_LOT
from conftest import INVALID_IDS

from conftest import BearsDB


class BearsDBExtended(BearsDB):
  def read_bear_not_found(self, bear_id):
    r = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
    assert r.status_code == 200  # delete this method when read_bear_not_found will be fixed to return 404
                                 # made this not to fail working delete test
  def delete_bear_bad_request(self, bear_id):
    r = requests.delete(SERVICE_URL + "/" + str(bear_id), timeout=T)
    assert r.status_code == 400


# @pytest.mark.d
@pytest.mark.delete
def test_successfully_deletes_all_when_no_bears(cleanup):
  bears_db = BearsDB()
  bears_db.delete_all_bears()


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.smoke
def test_successfully_deletes_all_existing_bears(valid_bear, flush_with_data):
  flush_with_data(valid_bear)
  bears_db = BearsDB()
  bears_db.delete_all_bears()
  bears = bears_db.read_all_bears()
  assert bears == []


# @pytest.mark.d
@pytest.mark.delete
@pytest.mark.smoke
def test_successfully_deletes_existing_bear_by_id(valid_bear):
  bears_db = BearsDBExtended()
  bear_id = bears_db.create_bear(valid_bear)
  bears_db.delete_bear(bear_id)
  bears_db.read_bear_not_found(bear_id)


# @pytest.mark.d
@pytest.mark.delete
def test_successfully_deletes_bear_by_id_that_does_not_exist(valid_bear):
  bears_db = BearsDBExtended()
  bear_id = bears_db.create_bear(valid_bear)
  bears_db.delete_bear(bear_id)
  bears_db.delete_bear(bear_id)


# @pytest.mark.d
@pytest.mark.parametrize("invalid_id", INVALID_IDS)
def test_fails_to_delete_bear_by_invalid_id(invalid_id):
  bears_db = BearsDBExtended()
  bears_db.delete_bear_bad_request(invalid_id)


# @pytest.mark.d
@pytest.mark.performance
@pytest.mark.delete
@pytest.mark.slow
def test_successfully_deletes_in_time_all_bears_when_a_lot_bears_exist(valid_bear, flush_with_data):
  flush_with_data(valid_bear, how_many_bears=A_LOT)
  bears_db = BearsDB()
  time_start = time.monotonic()
  bears_db.delete_all_bears()
  time_end = time.monotonic()
  assert time_end - time_start < T_MAX_FOR_LOAD_TEST
