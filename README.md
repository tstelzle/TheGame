# The Game

This will be a Python implementation of the board game "The Game".

There is a server, which will manage various games via an API.

The Client will repeately ask the server for new information and hence is able to play the game.

# Run

The Makefile commands, which are explained below, start the TechStack with the frontend-server, backend-api and the database.

## Requirements
You will need a docker-composer version >= 1.25.0. 
For this a docker version of >= 19 is recommended.

## Production
Copy the .env.prod.sample and rename it to .env.prod. Then set the username and password for the mongo database in the .env.prod file.
Afterwards run this command:
```shell
make run ENV=PROD
```

## Development
Copy the .env.prod.sample and rename it to .env.dev. Then set the username and password for the mongo database in the .env.dev file.
Afterwards run this command:
```shell
make run ENV=DEV
```

# API
The current API class can be tested and run with the Postman collection.
Currently not up to date, as a switch to Swagger is in progress.

[Collection](./TheGame.postman_collection.json)

# Commands

## Stop
This command will stop all running DEV and PROD containers.
```shell
make stop
```

## Down
This command will stop and remove all DEV and PROD containers.
```shell
make reset
```

# Python Client

This client is currently out of date, as a website is more preferred.

```shell
cd client
pip install -r requirements.txt
python3 client.py
```

## Create Executable

```shell
pip install pyinstaller
cd client
pyinstaller --onefile client.py
./dist/client &
```

