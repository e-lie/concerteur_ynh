# Le concerteur 


### Installation

* `virtualenv -p python3 venv
* edit `.env` to configure database login (tested with mysql)
* `source .env`
* `pip3 install -r requirements.txt`
* `python3 manage.py db init`
* `python3 manage.py db migrate`
* `python3 manage.py db upgrade`
* `apt-get install python3-docopt` (for the messageReception.py script to work outside venv)


LICENCE GPL
