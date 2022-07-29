@echo off

if not exist ./env/Scripts/activate (
    echo 'Creating virtual environment...'
    py -3.8 -m venv ./env || exit /b
)

echo 'Activating virtual environment...'
call ./env/Scripts/activate || exit /b

echo 'Upgrading pip...'
python -m pip install --upgrade pip || exit /b

echo 'Installing dependencies...'
pip install -r ./requirements.txt || exit /b

echo 'Running type checks...'
mypy --strict signal_ocean || exit /b

echo 'Running code analysis...'
flake8 signal_ocean || exit /b

echo 'Running tests...'
pytest || exit /b

echo 'Analyzing docstrings...'
pydocstyle --match='(?!_[^_]).*\.py' --convention=google signal_ocean || exit /b

echo 'Building dist...'
rmdir /S /Q dist/
python ./setup.py sdist bdist_wheel
