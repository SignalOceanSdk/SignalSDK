#!/bin/bash -e
set -euxo pipefail

while [[ "$#" -gt 0 ]]
do
    case $1 in
        --repository-url)
            repository_url="$2"
            shift 2
            ;;
        --username)
            username="$2"
            shift 2
            ;;
        --password)
            password="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

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

if [[ ! $repository_url ]]
then
    echo 'Repository URL was not provided.'
    exit 1
fi

if [[ ! $username ]]
then
    echo 'Username was not provided.'
    exit 1
fi

if [[ ! $password ]]
then
    echo 'Password was not provided.'
    exit 1
fi

twine upload --skip-existing --repository-url "$repository_url" -u "$username" -p "$password" ./dist/*
