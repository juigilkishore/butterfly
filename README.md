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

Database delete
---------------
Drop all the tables
```commandline
source butterfly-env/bin/activate
python butterfly.py --action db_drop --config etc/butterfly.conf
```

Run service
-----------
Run the butterfly service
```commandline
source butterfly-env/bin/activate
python butterfly.py --action run --config etc/butterfly.conf
```

API list
--------
##### User APIs

1. *GET*      **/user**               Retrieves all user details
2. *GET*      **/user/<user_id>**     Retrieves user <user_id>'s details
3. *POST*     **/user**               Creates a user
4. *PUT*      **/user/<user_id>**     Edits user <user_id>'s details
5. *DELETE*   **/user/<user_id>**     Delete user <user_id>

##### Lesson APIs

1. *GET*      **/lesson**                 Retrieves all lesson details
2. *GET*      **/lesson/<lesson_id>**     Retrieves lesson <lesson_id>'s details
3. *POST*     **/lesson**                 Creates a lesson
4. *PUT*      **/lesson/<lesson_id>**     Edits lesson <lesson_id>'s details
5. *DELETE*   **/lesson/<lesson_id>**     Delete lesson <lesson_id>

##### Goal APIs

1. *GET*      **/goal**               Retrieves all goal details
2. *GET*      **/goal/<goal_id>**     Retrieves goal <goal_id>'s details
3. *POST*     **/goal**               Creates a goal
4. *PUT*      **/goal/<goal_id>**     Edits goal <goal_id>'s details
5. *DELETE*   **/goal/<goal_id>**     Delete goal <goal_id>

##### Lesson Activity APIs

1. *GET*      **/user/<user_id>/activity/lesson**                 Retrieves all lesson activity details of <user_id>
2. *GET*      **/user/<user_id>/activity/lesson/<lesson_id>**     Retrieves lesson activity of <lesson_id>'s details for <user_id>
3. *POST*     **/user/<user_id>/activity/lesson**                 Creates a lesson activity <lesson_id> for <user_id>
4. *PUT*      **/user/<user_id>/activity/lesson/<lesson_id>**     Edits lesson activity <lesson_id>'s details for <user_id>
5. *DELETE*   **/user/<user_id>/activity/lesson/<lesson_id>**     Delete lesson activity <lesson_id>'s details for <user_id>

##### Goal Activity APIs

1. *GET*      **/user/<user_id>/activity/goal**               Retrieves all goal activity details of <user_id>
2. *GET*      **/user/<user_id>/activity/goal/<goal_id>**     Retrieves goal activity of <goal_id>'s details for <user_id>
3. *POST*     **/user/<user_id>/activity/goal**               Creates a goal activity <goal_id> for <user_id>
4. *PUT*      **/user/<user_id>/activity/goal/<goal_id>**     Edits goal activity <goal_id>'s details for <user_id>
5. *DELETE*   **/user/<user_id>/activity/goal/<goal_id>**     Delete goal activity <goal_id>'s details for <user_id>
