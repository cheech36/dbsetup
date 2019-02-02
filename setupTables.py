#!/usr/bin/env python3
import os
import sys
import psycopg2
import pandas as pd

def sanitize(dirtyName):
    clean_list = [char for char in dirtyName if char.isalnum()]
    name = ""
    for char in clean_list:
        name += char
    if(len(name) == 0):
        name = "col_error"
    return name
    
def gen_table_sql(df, key):
    dtypeMap = {"int64":"INTEGER", "object":"CHAR (200)", "float64":"FLOAT"} 
    sql = "CREATE TABLE %s (" % str.upper(sanitize(key))
    pg_types =  [dtypeMap[str(dftype)] for dftype in df.dtypes]

    for  col, pg_type in zip(df.columns, pg_types):
        sql += "%s %s," % (str.upper( sanitize(col)), pg_type)
        
    sql = sql.strip(',')
    sql += ');'
    return sql

project = sys.argv[1]
csv_cond = os.listdir(project)
files_csv = [x for x in csv_cond if x.find('.csv')]
tableNames = [x.strip('.csv') for x in files_csv]
tableMap = dict(zip(tableNames, files_csv))


dbname=sys.argv[2]
user=sys.argv[3]
password=sys.argv[4]

print("dbname: " + dbname)

conn = psycopg2.connect(dbname=dbname, user=user, password=password)
cur = conn.cursor()
autodrop_list = []

for key, val in tableMap.items():
    try:
        autodrop_list.append(str.upper( sanitize( key )))
        file_path = os.path.join(project,str(val))
        df = pd.read_csv(file_path)
        sql = gen_table_sql(df, key)
        print("Creating table %s" % str.lower(key))
        cur.execute(sql)
        with open(file_path, 'r') as csvFile:
            next(csvFile) #https://www.dataquest.io/blog/loading-data-into-postgres/
            cur.copy_from(csvFile, key, sep=',', null='')
            conn.commit()

    except Exception as ex:
        print("could not create table %s from %s " % (key,val))        
        print("The error is %s" % ex)
        autodrop_list.remove(str.upper( sanitize( key )))
        # If we get an exception we want to commit, close and reopen
        # our cursor so that our errors do not "pile up"
        # https://stackoverflow.com/questions/10399727/psqlexception-
        # current-transaction-is-aborted-commands-ignored-until-end-of-tra
        # Electing for option 2 
        conn.close() # End this transaction because it has a malformed query
        # Start a fresh transaction
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)
        cur = conn.cursor()

conn.commit()
conn.close()

with open('autodrop.sh', 'w') as dropfile:
    dropfile.write("#/bin/bash\n\n")
    dropfile.write("psql -h localhost -d %s -U %s -c '''\n" % (dbname, user))
    for table in autodrop_list:
        line = "DROP TABLE %s;\n" % table
        dropfile.write(line)
    dropfile.write("'''")
