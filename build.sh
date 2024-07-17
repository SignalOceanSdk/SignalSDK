#!/bin/bash -e

if [[ ! -f ./env/bin/activate ]]
then
    echo 'Creating virtual environment...'
    python3.8 -m venv ./env
fi

echo 'Activating virtual environment...'
source ./env/bin/activate

echo 'Upgrading pip...'
python -m pip install --upgrade pip

echo 'Installing dependencies...'
pip install -r ./requirements.txt

echo 'Running type checks...'
mypy  signal_ocean

echo 'Running code analysis...'
flake8 signal_ocean

echo 'Running tests...'
pytest

echo 'Analyzing docstrings...'
pydocstyle --match='(?!_[^_]).*\.py' --convention=google signal_ocean

echo 'Building dist...'
rm -rf dist/*
python ./setup.py sdist bdist_wheel
