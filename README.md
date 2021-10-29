# The Game

This will be a Python implementation of the board game "The Game".

There is a server, which will manage various games via an API.

The Client will repeately ask the server for new information and hence is able to play the game.

# Run

Copy the .env.prod.sample and rename it to .env.prod. Then set the username and password for the mongo database in the .env.prod file.
Afterwards run this command:

```shell
docker-compose --env-file .env.prod up -d
```

## Server

```shell
cd server
pip install -r requirements.txt
python3 server.py
```

### API

The current API class can be tested and run with the Postman collection.

[Collection](./TheGame.postman_collection.json)



## Client

```shell
cd client
pip install -r requirements.txt
python3 client.py
```

### Create Executable

```shell
pip install pyinstaller
cd client
pyinstaller --onefile client.py
./dist/client &
```

