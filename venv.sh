#/bin/bash

set -x

virtualenv venv --python=/usr/bin/python3 --system-site-packages
source venv/bin/activate
pip3 install numpy
pip3 install psycopg2
pip3 install pandas
