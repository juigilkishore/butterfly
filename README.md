Butterfly
=========

Download
--------
git clone git@github.com:juigilkishore/butterfly.git
cd butterfly

Install Dependencies
--------------------
sudo apt-get install python-virtualenv $(cat dependencies.txt)
virtualenv butterfly-env
source butterfly-env/bin/activate
pip install -r requirements.txt

Database creation
-----------------
mysql -uroot -p<root-password>
mysql> CREATE DATABASE butterfly;
mysql> GRANT ALL PRIVILEGES ON butterfly.* TO 'butterflyuser'@'localhost' IDENTIFIED BY 'butterflypass';
mysql> GRANT ALL PRIVILEGES ON butterfly.* TO 'butterflyuser'@'%' IDENTIFIED BY 'butterflypass';

mysql -ubutterflyuser -pbutterflypass
mysql> USE butterfly

Edit Configuration
------------------
Edit "connection" in "Database" section in the etc/butterfly.conf configuration file with
butterfly database's username and password

Database initialization
-----------------------
source butterfly-env/bin/activate
python butterfly.py --action db_init --config etc/butterfly.conf

Database deletion
-----------------
source butterfly-env/bin/activate
python butterfly.py --action db_drop --config etc/butterfly.conf

Run service
-----------
TODO
