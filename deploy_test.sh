#!/bin/bash

CODE_DIR=`pwd`
TEST_DIR=~/tmp/pyinktest

# preparing test dir
rm -rf ${TEST_DIR}
mkdir ${TEST_DIR}
cp -r templates ${TEST_DIR}/templates
cp -r demo_helloworld.py ${TEST_DIR}/
cp -r demo_piechart.py ${TEST_DIR}/
mkdir ${TEST_DIR}/output

# install pyinkscape package
python3 -m venv ${TEST_DIR}/.env
. ${TEST_DIR}/.env/bin/activate
python setup.py install
# pip install -r requirements.txt

# run demo
cd ${TEST_DIR}
python demo_helloworld.py
python demo_piechart.py

