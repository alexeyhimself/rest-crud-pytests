"""

  Tests in this file

  Post-Deployment Verification:
    * /info page is displayed when service works: test_info_page_is_displayed
    * Delete (even when no bears in system) works: test_delete_all_works_when_no_bears

"""

import pytest
import requests

from conftest import URL, T
from conftest import BearsDB


# @pytest.mark.d
@pytest.mark.pdv
def test_info_page_is_displayed():
  r = requests.get(URL + '/info', timeout=T)
  assert r.status_code == 200
  assert len(r.text) > 0


# @pytest.mark.d
@pytest.mark.pdv
def test_delete_all_works_when_no_bears():
  bears_db = BearsDB()
  bears_db.delete_all_bears()
