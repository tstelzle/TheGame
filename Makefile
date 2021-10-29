# MAKEFILE https://github.com/tstelzle/TheGame
# AUTHORS: Tarek Stelzle

-include .env.prod

production:
	docker-compose -f docker-compose-dev.yml stop
	docker network create $(DEFAULT_EXT_NET) || true
	docker network create $(PROXY_NET) || true
	docker-compose --env-file .env.prod -f docker-compose-prod.yml up --force-recreate --build -d

development:
	docker-compose -f docker-compose-prod.yml stop
	docker-compose --env-file .env.dev -f docker-compose-dev.yml up --force-recreate --build -d

stop:
	docker-compose -f docker-compose-dev.yml stop
	docker-compose -f docker-compose-prod.yml stop
