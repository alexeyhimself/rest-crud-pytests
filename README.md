REST CRUD PyTests
===========================
This is a set of PyTest tests for simple REST CRUD service, made with test plan and report


# Getting Started
## Prerequisites
* `git` is installed
* `docker` is installed and is running

## Read the test plan
File test_plan.txt contains the plan on how to test REST CRUD service. Part of this plan is related to these auto tests.

## How to run tests
### Get tested app
```
# pull and run tested application
docker pull azshoo/alaska:1.0
docker run -p 8091:8091 --rm azshoo/alaska:1.0
```
### Get tests and get them ready:
```
# get source code
git clone https://github.com/alexeyhimself/rest-crud-pytests.git

# init virtualenv
python3 -m venv ./rest-crud-pytests/
cd ./rest-crud-pytests/
source bin/activate

# install required python libs
pip3 install -r install/requirements.txt
```

### Run PDV tests
In `rest-crud-pytests` folder run:
```
pytest -v -m pdv
```
All tests must get PASSED status

### Run other tests
In `rest-crud-pytests` folder run:
```
pytest -v -m run_on_empty
pytest -v -m smoke
pytest -v -m 'not slow and not smoke and not run_on_empty'
pytest -v -m slow
```
All tests must get PASSED status

## Reports
If you don't want to run tests then you can look at the `rest-crud-pytests/reports` folder. It contains reports from last local run:
* `report_tests.txt` - contains short test execution info for the tests
* `report_logs.txt` - contains short cuts from logs for `WARN` and `ERR` messages in tested app logs during test runs

### Overall tests report is the following:
* pdv: 1 passed
* run_on_empty: 2 passed
* smoke: 5 passed
* not slow and not smoke and not run_on_empty: 150 failed, 28 passed
* slow: 2 passed

### Overall logs report is the following:
* WARNING - 2 unique log messages
* ERROR - 12 unique log messages
