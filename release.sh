#!/bin/bash -e

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

if [[ ! -f ./env/bin/activate ]]
then
    echo 'Virtual environment does not exist. Run build.sh to create it.'
    exit 1
fi

source ./env/bin/activate
twine upload --repository-url "$repository_url" -u "$username" -p "$password" ./dist/*
