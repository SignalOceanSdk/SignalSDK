#!/bin/bash -e
set -euxo pipefail

echo 'Upgrading pip...'
python3.8 -m pip install --upgrade pip

echo 'Installing dependencies...'
pip install -r ./requirements.txt

echo 'Running type checks...'
mypy --strict --implicit-reexport signal_ocean

echo 'Running code analysis...'
flake8 signal_ocean

echo 'Running tests...'
pytest

echo 'Analyzing docstrings...'
pydocstyle --match='(?!_[^_]).*\.py' --convention=google signal_ocean

echo 'Building dist...'
rm -rf dist/*
python3.8 ./setup.py sdist bdist_wheel

echo 'Installing SDK...'
pip install -e .

echo 'Installing dependencies...'
pip install notebook jupyter matplotlib openpyxl seaborn folium sqlalchemy pandas strictly_typed_pandas --upgrade

echo 'Running notebooks...'
ls -LR | grep .ipynb | while read filename
do
  if [ -z "${SIGNAL_OCEAN_API_KEY}" ]
    then echo 'Error: SIGNAL_OCEAN_API_KEY has not been defined'
    exit 1
  fi
  echo "$filename"
  jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"
done