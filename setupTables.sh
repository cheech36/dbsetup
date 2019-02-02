#/bin/bash

CSVDIR="data"
DBNAME=$1
ZIPFILE=$2
USER="$(whoami)"
PASSWORD="none"

if [ ! -d "$CSVDIR" ]; then
    mkdir $CSVDIR
    unzip $ZIPFILE -d $CSVDIR
fi

source venv/bin/activate
./setupTables.py $CSVDIR $DBNAME $USER $PASSWORD
