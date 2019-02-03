dbsetup

These scripts are used to automate the process of converting flat csv files into a set of relational database tables.


Usage:

	1) Create the database using postgres user assigning ownership to user:
	   i)  sudo su postgres
	   ii) createdb -O <username> <dbname>
	   
	2) To install the dependencies in a virtual enviornment run:
	   i) ./venv.sh
	   ii) By default venv will use existing installation. To disable
	       remove --system-site-packages

	3) ./setupTables.sh <dbname> <zipfile> 
	   i) If connecting to local database use "localhost"
	   ii) Change username and password 

	4) Optional: if you wish to delete the tables:
	   chmod 600 autoDrop.sh
	   ./autoDrop.sh


Output:

	1) Extracted csv files will be stored in "data" directory.
	2) Some tables may fail to build, these will be listed at runtime.
	
      


