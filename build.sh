#!/bin/bash -e

if [[ ! -f ./env/bin/activate ]]
then
    echo 'Creating virtual environment...'
    python3.8 -m venv ./env
fi

source ./env/bin/activate
pip install -r ./requirements.txt
pytest

rm -rf dist/*
python3.8 ./setup.py sdist bdist_wheel
