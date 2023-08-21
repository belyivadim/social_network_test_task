# Simple social network API

The application has functionality for registrating users, login users, creating and liking/unliking posts.
All information about api can be found in specification in ./src/swagger.yml file (also swagger UI is accessible on address http://localhost:8080/api/ui/).

### Run
To run the application simply execute the command:
```bash
docker-compose up --build
```


## Automated bot
The bot demonstrates functionalities of the API. It registrates users, makes some posts, and likes/unlikes them.
The bot can be configured with ./src/bot/config.yml file.

### Run
To run the bot simply execute the following commands:
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./src/bot/requirements.txt
python3 ./src/bot/bot.py
```
Note you should run the bot only while application is runnig.
