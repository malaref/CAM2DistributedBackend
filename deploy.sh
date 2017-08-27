#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir --parents build
cp --recursive $DIR/src/* build
cd build
zip --move --recurse-paths --quiet core/cam2.zip core/analyzer core/camera core/util
export FLASK_APP=flask_api/main.py
python -m flask run
