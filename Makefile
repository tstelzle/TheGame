# MAKEFILE https://github.com/tstelzle/TheGame
# AUTHORS: Tarek Stelzle

production:
	docker-compose -f docker-compose-dev.yml stop
	docker-compose --env-file .env.prod -f docker-compose-prod.yml up --force-recreate --build -d


development:
	docker-compose -f docker-compose-prod.yml stop
	docker-compose --env-file .env.dev -f docker-compose-dev.yml up --force-recreate --build -d
