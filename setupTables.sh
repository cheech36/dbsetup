#/bin/bash

CSVDIR="data"
DBNAME=$1
ZIPFILE=$2
HOST="REPLACE ME"
USER="REPLACE ME"
PASSWORD="REPLACE ME"

if [ ! -d "$CSVDIR" ]; then
    mkdir $CSVDIR
    unzip $ZIPFILE -d $CSVDIR
fi

source venv/bin/activate
./setupTables.py $CSVDIR $HOST $DBNAME $USER $PASSWORD
