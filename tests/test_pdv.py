import pytest
import requests

from conftest import URL, T


# @pytest.mark.d
@pytest.mark.pdv
def test_info_page_is_displayed():
  r = requests.get(URL + '/info', timeout=T)
  assert r.status_code == 200
  assert len(r.text) > 0