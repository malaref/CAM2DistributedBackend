#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_FOLDER=".CAM2DistributedBackend"

echo '>>>> Cleaning up'
cd
rm -rf $INSTALL_FOLDER

echo '>>>> Preparing files'
mkdir $INSTALL_FOLDER
cp --recursive $DIR/* $INSTALL_FOLDER
cd $INSTALL_FOLDER/CAM2DistributedBackend/resources/spark
zip --move --recurse-paths --quiet cam2.zip analyzer camera util
cd ../../../

echo '>>>> Installing CAM2DistributedBackend'
sudo pip install --editable .
