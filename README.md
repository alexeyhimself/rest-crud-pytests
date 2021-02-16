REST CRUD PyTests
===========================
This is a set of PyTest tests for simple REST CRUD service, made with test plan and report


# Getting Started
## Prerequisites
* git is installed
* docker is installed and running

## How to install
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

## Run PDV tests
In `rest-crud-pytests` folder run:
```
pytest -v -m pdv
```
All tests must get PASSED status

## Run other tests
In `rest-crud-pytests` folder run:
```
pytest -v -m smoke
pytest -v -m 'not slow and not smoke and not run_on_empty'
pytest -v -m slow
```
All tests must get PASSED status
