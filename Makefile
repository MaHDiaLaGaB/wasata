.env:  ## Ensures that env file exists
	@cp -n .env.example .env

include .env
export


define print_section
	echo ""
	echo "<==><==><==><==><==><==><==><==><==>"
	echo "$(1)"
	echo "<==><==><==><==><==><==><==><==><==>"
endef

directories:= ./ ./dev-database


#
# Misc
#
help:  ##  print help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ": .*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


build-images:  ##  Build all images
	echo "Building images"
	make start-db
	make start-api
	make start-payment


start-api:  ## build docker images
	echo "Building images"
	docker build -t wasata/api .

start-payment:
	echo "Building mo3amalat"
	docker build -t wasata/moamalat ./mo3amalat

start-db:
	echo "Building database"
	cd dev-database && make image-db

up:  ## build docker containers
	docker-compose -f docker-compose.yml up -d

reset:
	@make stop
	sleep 1
	@make build-images
	sleep 1
	@make up


stop:  ## stop the active docker containers
	docker-compose down



db-create-revision:  ## create alembic revision for database
	alembic revision --autogenerate -m "$(title)"

db-create-migration:  ## create alembic database migrations
	alembic --name alembic upgrade head


check-format:
	black --check .

format-fix:
	black .

lint:
	mypy --explicit-package-bases --config-file  mypy.ini

create-admin-key:
	@PYTHONPATH=. python3 app/tools/my_cli.py

change-usdt-price:
	@PYTHONPATH=. python3 app/tools/change_price.py