REST CRUD PyTests
===========================
This is a set of PyTest tests for simple REST CRUD service, made with test plan and report


# Getting Started
## Prerequisites
* `git` is installed
* `docker` is installed and is running

## Read the test plan
File `test_plan.txt` contains the plan on how to test REST CRUD service. Part of this plan is related to these auto tests.

## How to run tests
### Get tested app
```
# pull and run tested application
docker pull azshoo/alaska:1.0
docker run -d -p 8091:8091 --name alaska --rm azshoo/alaska:1.0

# view docker container logs
docker logs alaska -f
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
To make sure that everything is ready for test execution, run Post-Deployment Verification (PDV) tests. To do so in `rest-crud-pytests` folder run:
```
pytest -v -m pdv
```
All tests must get `PASSED` status

### Run ALL the tests
When PDV tests passed, then you can run all the other tests. To do so in `rest-crud-pytests` folder run:
```
pytest -v -m smoke
pytest -v -m 'not slow and not smoke and not pdv'
pytest -v -m slow
```
All tests must get `PASSED` status

## Reports
If you don't want to run tests then you can look at the `rest-crud-pytests/reports` folder. It contains reports from last local run:
* `report_tests.txt` - contains short test execution info for the tests
* `report_logs.txt` - contains short cuts from logs for `WARN` and `ERR` messages in tested app logs during test runs

### Overall tests report is the following:
* `pdv`: 2 passed
* `smoke`: 5 passed
* `not slow and not smoke and not pdv`: 160 failed, 31 passed
* `slow`: 2 passed

### Overall logs report is the following:
* `WARNING` - 2 unique log messages
* `ERROR` - 12 unique log messages

## Finish testing
To stop running container of tested app run:
```
docker stop alaska
```
To deactivate virtualenv in `rest-crud-pytests` folder run:
```
deactivate
```
