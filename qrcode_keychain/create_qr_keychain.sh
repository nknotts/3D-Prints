#!/bin/bash

set -e
set -u

# change to appropriate path for your system
OPENSCAD=/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD
QRCODE_PAYLOAD="Mr P and Sharkboy!"
DIRECTORY_SUFFIX="testing"

# change current working directory to location of this script file
# this will be where the virtual environment will be created
THIS_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
pushd "$THIS_DIR" > /dev/null

# if virtual environment does not exist, create it and install requirements
if [[ ! -d env ]]; then
    echo "Setting up virtualenv"
    python3 -m venv env
    env/bin/python3 -m pip install -r requirements.txt
fi

# generate output in its own folder
OUTPUT_DIR="$THIS_DIR"/output/$(date "+%Y-%m-%d_%H-%M-%S")-$DIRECTORY_SUFFIX
mkdir -p "$OUTPUT_DIR"
pushd "$OUTPUT_DIR" > /dev/null

echo "Generating OpenSCAD"
"$THIS_DIR"/env/bin/python3 "$THIS_DIR"/create_qr_keychain_openscad.py "$QRCODE_PAYLOAD"

echo "Generating STL"
$OPENSCAD keychain_qr_code.scad --export-format binstl -o keychain_qr_code.stl

