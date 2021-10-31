# MAKEFILE https://github.com/tstelzle/TheGame
# AUTHORS: Tarek Stelzle

ENV := PROD

ifeq "$(ENV)" "PROD"
include .env.prod
else
include .env.dev
endif

test:
	@if [ $(ENV) = PROD ]; then \
		echo $(ENV); \
	elif [ $(ENV) = DEV ]; then \
		echo $(ENV); \
	else \
		echo "else"; \
	fi

run:
	@if [ $(ENV) = PROD ]; then \
	    echo "PROD"; \
		docker-compose -f docker-compose-dev.yml stop; \
		docker network create $(DEFAULT_EXT_NET) || true; \
		docker network create $(PROXY_NET) || true; \
		docker-compose --env-file .env.prod -f docker-compose-prod.yml up --force-recreate --build -d; \
	elif [ $(ENV) = DEV ]; then \
	    echo "DEV"; \
		docker-compose -f docker-compose-prod.yml stop; \
		docker-compose --env-file .env.dev -f docker-compose-dev.yml up --force-recreate --build -d; \
	else \
		echo "Wrong ENV - Choose DEV or PROD."; \
	fi

stop:
	-docker-compose -f docker-compose-dev.yml stop
	-docker-compose -f docker-compose-prod.yml stop

reset:
	-docker-compose -f docker-compose-dev.yml down
	-docker-compose -f docker-compose-prod.yml down
