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

echo 'Upgrading pip...'
python3.8 -m pip install --upgrade pip

echo 'Installing dependencies...'
pip install -r ./requirements.txt

echo 'Running type checks...'
mypy  --implicit-reexport signal_ocean

echo 'Running code analysis...'
flake8 signal_ocean

echo 'Running tests...'
pytest

echo 'Analyzing docstrings...'
pydocstyle --match='(?!_[^_]).*\.py' --convention=google signal_ocean

# Isolate dev form release build env
echo "Creating virtual environment for building release"
python3.8 -m venv release-env
source release-env/bin/activate

# Build on virtual environment
echo "Building dist with env $(echo $VIRTUAL_ENV)..."
echo "Python: $(which python)"
echo "Pip: $(which pip)"

# Install version of wheel from dev requirements
pip install $(grep -Po '^wheel.*$' ./requirements.txt)

rm -rf dist/*
python ./setup.py sdist bdist_wheel

echo "Deactivating virtual environment"
deactivate

# Clean up virtual environment
echo "Removing virtual environment"
rm -rf release-env

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

twine upload --verbose --skip-existing --repository-url "$repository_url" -u "$username" -p "$password" ./dist/*
