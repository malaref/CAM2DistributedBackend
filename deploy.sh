#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEPLOY_FOLDER="build"

echo '>>>> Cleaning up'
rm -rf $DEPLOY_FOLDER

echo '>>>> Preparing files'
mkdir $DEPLOY_FOLDER
cp --recursive $DIR/src/* build
cd build/core
zip --move --recurse-paths --quiet cam2.zip analyzer camera util
cd ..

echo '>>>> Creating the database'
cat $DIR/db.sql | sqlite3 database.db

echo '>>>> Launching Flask'
export FLASK_APP=flask_api
pip install -e .
python -m flask run
