import pytest
import requests
import random
import string
import json
import threading
import sys

from pydantic import BaseModel
from typing import Any, Callable


URL = "http://0.0.0.0:8091"
SERVICE_URL = URL + "/bear"
BEAR_DEFAULT_PARAMS = ["bear_type", "bear_name", "bear_age"]
FINE_LENGTH_OF_BEAR_NAME = 10
BEAR_AGES = range(0, 51)  # in average 25, but 50 is a maximum lifetime expectancy for bears in captivity (except GUMMY)
T_MAX_FOR_LOAD_TEST = 1   # [seconds], maximum time to wait for high load
T = 10                    # [seconds], timeout for requests
A_LOT = 10000             # minimum number of bear records to expect in "flush a lot" tests
A_FEW = 10                # minimum number of bear records to expect in "flush a few" tests


VALID_BEAR_NAMES = [
  "mikhail",              # lowercase
  "Mikhail",              # case sensitive
  "MIKHAIL",              # uppercase
  "First Last",           # with space separator
  "&\'-_ \"+?!",          # contains special symbols
  "Михаил",               # Cyrillic
  "成對",                  # hieroglyph
  "زوجي"                  # Arabic
]

INVALID_BEAR_NAMES = [
  "",                     # empty string
  " ",                    # looks like empty string
  None,                   # Python special value
  True,                   # Python special value
  False,                  # Python special value
  0,                      # special value
  10,                     # digit as digit
  "a"*1000,               # longest personal name in the world up to beginning of 2021 was 747 chars
  "name';DROP bears;--"   # SQL injection
]


VALID_BEAR_AGES = [
  BEAR_AGES[0],           # lowest
  BEAR_AGES[-1],          # highest
  BEAR_AGES[1],           # something in between
  1.2,                    # float
  1.123456                # high precission float (not specified limit of precission)
]

INVALID_BEAR_AGES = [
  "",                     # empty string
  "age",                  # word
  None,                   # Python special value
  True,                   # Python special value
  False,                  # Python special value
  BEAR_AGES[0] - 1,       # lower, than lowest
  BEAR_AGES[-1] + 1,      # higher than highest
  -1,                     # negative
  -1.2,                   # negative float
  1.12345678901234567890, # too high precission (not specified limit of precission)
  10e10,                  # too big value
  "1;DROP bears;--"       # SQL injection
]

VALID_BEAR_TYPES = [      # by specification at /info
  "POLAR",
  "BROWN",
  "BLACK",
  "GUMMY"
]

INVALID_BEAR_TYPES = [
  "WHITE",                # word not from VALID_BEAR_TYPES list 
  "black",                # another case of word from VALID_BEAR_TYPES list
  "",                     # empty string
  None,                   # Python special value
  0,                      # special value
  True,                   # Python special value
  False,                  # Python special value
  "POLAR';DROP bears;--"  # SQL injection
]

INVALID_IDS = [
  "",                     # empty string
  "word",                 # not a number
  -1,                     # negative number
  1.9,                    # float number
  "1,2",                  # several numbers at a time
  None,                   # Python special value
  0,                      # special value
  True,                   # Python special value
  False,                  # Python special value
  sys.maxsize + 1,        # pretends to be out-of-range number
  "1;DROP bears;--"       # SQL injection
]

INVALID_DATASET = [
  {},                     # empty dict
  json.dumps({}),         # empty as valid payload
  [],                     # not a dict
  None,                   # not a dict, Python special value
  # True,                 # not a dict, boolean to agree (requests can't send, so disabled)
  False,                  # not a dict, boolean to disagree
  "word",                 # not a dict
  # 1,                    # not a dict, integer (requests can't send, so disabled)
  0                       # not a dict, special value
]


@pytest.fixture
def valid_bear(valid_bear_types: list, valid_bear_name: str, valid_bear_ages: range) -> dict:
  bear_type = random.choice(valid_bear_types)
  bear_name = valid_bear_name
  bear_age = random.choice(valid_bear_ages)
  return {"bear_type": bear_type, "bear_name": bear_name, "bear_age": bear_age}


@pytest.fixture
def valid_bear_types() -> list:
  return VALID_BEAR_TYPES


 # Used from: https://pynative.com/python-generate-random-string
@pytest.fixture
def valid_bear_name() -> str:
  letters = string.ascii_letters
  return ''.join(random.choice(letters) for i in range(FINE_LENGTH_OF_BEAR_NAME))


@pytest.fixture
def valid_bear_ages() -> range:
  return BEAR_AGES


# Used pass parameter to fixture approach from: 
# https://stackoverflow.com/questions/18011902/pass-a-parameter-to-a-fixture-function
@pytest.fixture
def flush_with_data(valid_bear: dict) -> Callable[[dict, int], None]:
  def flush(valid_bear: dict, how_many_bears: int = A_FEW) -> None:
    threads = list()
    for i in range(0, how_many_bears):
      t = threading.Thread(
        target=requests.post,
        args=(SERVICE_URL,),
        kwargs={
          "data": json.dumps(valid_bear),
          "timeout": T
        }
      )
      t.start()
      threads.append(t)
  
    for each_thread in threads:
      each_thread.join()

  return flush


@pytest.fixture
def cleanup() -> None:
  r = requests.delete(SERVICE_URL, timeout=T)


class Bear(BaseModel):
  bear_id: int
  bear_name: str
  bear_type: str
  bear_age: float
  
  # used __post_init___ analog for dataclass from
  # https://github.com/samuelcolvin/pydantic/issues/691
  def __init__(self, **data: Any):
    super().__init__(**data)
    assert self.bear_type in VALID_BEAR_TYPES
    assert self.bear_age >= BEAR_AGES[0]
    assert self.bear_age <= BEAR_AGES[-1]


class BearsDB:
  def create_bear(self, bear: dict) -> str:
    r = requests.post(SERVICE_URL, data=json.dumps(bear), timeout=T)
    assert r.status_code == 200
    assert r.text.isdigit() == True
    return r.text

  def read_bear(self, bear_id: int) -> dict:
    r = requests.get(SERVICE_URL + "/" + str(bear_id), timeout=T)
    assert r.status_code == 200
    bear = json.loads(r.text)
    assert isinstance(bear, dict) == True
    Bear(**bear)  # data basic validation
    return bear

  def read_all_bears(self) -> list:
    r = requests.get(SERVICE_URL, timeout=T)
    assert r.status_code == 200
    bears = json.loads(r.text)
    assert isinstance(bears, list) == True
    return bears

  def update_bear(self, bear_id: int, params: dict) -> None:
    r2 = requests.put(SERVICE_URL + "/" + str(bear_id), data=json.dumps(params), timeout=T)
    assert r2.status_code == 200
    assert r2.text == "OK"

  def delete_bear(self, bear_id: int) -> None:
    r = requests.delete(SERVICE_URL + "/" + str(bear_id), timeout=T)
    assert r.status_code == 200
    assert r.text == "OK"

  def delete_all_bears(self) -> None:
    r = requests.delete(SERVICE_URL, timeout=T)
    assert r.status_code == 200
    assert r.text == "OK"

