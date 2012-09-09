#!/bin/bash
virtualenv venv
. venv/bin/activate
pip install --log pip.log ./kleindemo.pybundle 
cd kleindemo
python main.py >> ../mainpy.log
