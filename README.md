Butterfly
=========

Download
--------
```commandline
git clone git@github.com:juigilkishore/butterfly.git
cd butterfly
```

Install Dependencies
--------------------
```commandline
sudo apt-get install python-virtualenv $(cat dependencies.txt)
virtualenv butterfly-env
source butterfly-env/bin/activate
pip install -r requirements.txt
```

Database creation
-----------------
For MySQL database
```commandline
mysql -uroot -p
mysql> CREATE DATABASE butterfly;
mysql> GRANT ALL PRIVILEGES ON butterfly.* TO 'butterflyuser'@'localhost' IDENTIFIED BY 'butterflypass';
mysql> GRANT ALL PRIVILEGES ON butterfly.* TO 'butterflyuser'@'%' IDENTIFIED BY 'butterflypass';

mysql -ubutterflyuser -p
mysql> USE butterfly;
```

For SQLite database
```commandline
touch butterfly.db
```

Edit Configuration
------------------
Edit "connection" key in "Database" section in the etc/butterfly.conf configuration file

For MySQL database
```commandline
connection=mysql+mysqldb://<butterflyuser>:<butterflypass>@localhost/<butterfly-db-name>
```

For SQLite database
```commandline
connection=sqlite:///butterfly.db
```

Database initialize
-------------------
Create all the tables and populate with initial values
```commandline
source butterfly-env/bin/activate
python butterfly.py --action db_init --config etc/butterfly.conf
```

Database populate
-----------------
Update the tables with new values
```commandline
source butterfly-env/bin/activate
python butterfly.py --action db_add --config etc/butterfly.conf
```

Database delete
---------------
Drop all the tables
```commandline
source butterfly-env/bin/activate
python butterfly.py --action db_drop --config etc/butterfly.conf
```

Run service
-----------
TODO
