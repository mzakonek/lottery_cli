*** CLI LOTTERY APP ***

App is using sqlite3 db, which is created by ORM technique and queried by cursor. 

Functionalities:

- add person to lottery 
- add predicted number
- add json file with guidelines

Json file is holding lottery parameters:
1. numbers-quantity - amount of winning numbers
2. numbers-range - range of winning numbers
3. prize-pool 



Before running app.py in console, create db with following steps:

	1. instal requirements.txt in your venv
	2. run create_tables.py

