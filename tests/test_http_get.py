"""

  Tests in this file

  Reads without ID:
    * Read when no bears in system works: test_successfully_reads_all_bears_when_bears_not_exist
    * Read when 2+ bears in system works: test_successfully_reads_all_bears_when_bears_exist
    * Read when A LOT bears in system works: test_successfully_reads_all_bears_when_a_lot_bears_exist

  Reads with ID:
    * Read bear by valid existing ID works: test_successfully_reads_existing_bear_by_id
    * Read bear by valid non-existing ID works: test_fails_to_read_bear_by_valid_id_that_does_not_exist
    * Read bear by various invalid IDs works: test_fails_to_read_bear_by_invalid_id

  Data consistency:
    * Read returns what was Created: test_read_json_is_the_same_as_post_json

  Other:
    * HTTP 404 is displayed when try to open unknown URL path: test_gets_404_when_open_page_that_does_not_exist

"""

import pytest
import requests
import time

from conftest import SERVICE_URL, T, T_MAX_FOR_LOAD_TEST, A_LOT, A_FEW
from conftest import INVALID_IDS, URL

from conftest import BearsDB


class BearsDBExtended(BearsDB):
  def read_bear_not_found(self, bear_id):
    r = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
    assert r.status_code == 404  # why returns HTTP 200, not 400 bad request or 404 not found?
                                 # if HTTP 200, then why returns word EMPTY rather than []?
                                 # considering this 200 as a bug for HTTP REST


# @pytest.mark.d
def test_gets_404_when_open_page_that_does_not_exist(cleanup):
  r = requests.get(URL + "/unknown", timeout=T)
  assert r.status_code == 404


# @pytest.mark.d
def test_successfully_reads_all_bears_when_bears_not_exist(cleanup):
  bears_db = BearsDB()
  bears = bears_db.read_all_bears()
  assert bears == []


# @pytest.mark.d
@pytest.mark.smoke
def test_successfully_reads_all_bears_when_bears_exist(valid_bear):
  bears_db = BearsDB()
  bears_db.flud_with_bears(valid_bear)
  bears = bears_db.read_all_bears()
  assert len(bears) >= A_FEW


# @pytest.mark.d
@pytest.mark.slow
@pytest.mark.performance
def test_successfully_reads_in_time_all_bears_when_a_lot_bears_exist(valid_bear):
  bears_db = BearsDB()
  bears_db.flud_with_bears(valid_bear, how_many_bears=A_LOT)
  time_start = time.monotonic()
  bears = bears_db.read_all_bears()
  time_end = time.monotonic()
  assert len(bears) >= A_LOT
  assert time_end - time_start < T_MAX_FOR_LOAD_TEST
  

# @pytest.mark.d
@pytest.mark.parametrize("invalid_id", INVALID_IDS)
def test_fails_to_read_bear_by_invalid_id(invalid_id):
  bears_db = BearsDBExtended()
  bears_db.read_bear_not_found(invalid_id)


# @pytest.mark.d
def test_fails_to_read_bear_by_valid_id_that_does_not_exist(valid_bear):
  bears_db = BearsDBExtended()
  bear_id = bears_db.create_bear(valid_bear)
  bears_db.delete_bear(bear_id)
  bears_db.read_bear_not_found(bear_id)


# @pytest.mark.d
@pytest.mark.smoke
def test_successfully_reads_existing_bear_by_id(valid_bear):
  bears_db = BearsDBExtended()
  bear_id = bears_db.create_bear(valid_bear)
  bears_db.read_bear(bear_id)


# @pytest.mark.d
def test_read_json_is_the_same_as_post_json(valid_bear):
  bears_db = BearsDBExtended()
  bear_id = bears_db.create_bear(valid_bear)
  bear = bears_db.read_bear_not_found(bear_id)
  valid_bear["bear_id"] = bear_id
  assert bear == valid_bear
