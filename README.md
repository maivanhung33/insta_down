# insta_down
## install library 
run pip install -r requirements.txt
## connect database
change value of varibale in file /insta_down/insta_down/module/mongo_client.py or pass by command export <variable_name>=<value>
value need change: host, port, username, password, db, auth_source

*for cloud enable code in line 28-31*
### runserver
run python manage.py runserver
