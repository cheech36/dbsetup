#/bin/bash

virtualenv venv --python=/usr/bin/python3
source venv/bin/activate
pip3 install psycopg2
pip3 install pandas
