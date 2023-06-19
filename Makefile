.env:  ## Ensures that env file exists
	@cp -n .env.example .env

include .env
export

docker-project-name := wasata-api

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
	make build-db
	make build-api
	make build-payment


build-api:  ## build docker images
	echo "Building images"
	docker build -t wasata/api .

build-payment:  ## build moamalat payment image
	echo "Building mo3amalat"
	docker build -t wasata/moamalat ./mo3amalat

build-db:  ## build database image
	echo "Building database"
	docker build -t wasata/dev-postgres ./dev-database

dev-start-db:
	docker run wasata/dev-postgres

dev-start:  ## build docker containers for dev environment
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/dev.yml --profile dev up -d

demo-start:  ## build docker containers for demo environment
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/demo.yml --profile demo up -d

reset:
	@make stop
	sleep 1
	@make build-images
	sleep 1
	@make up


stop:
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/demo.yml down --remove-orphans --volumes

#
# ------------------------------- Database Locally-----------------------------------
#
# development
db-create-revision-dev:  ## create alembic revision for development database
	alembic -c alembic-dev.ini revision --autogenerate -m "$(title)"

db-create-migration-dev:  ## create alembic database migrations in development
	alembic -c alembic-dev.ini upgrade head


#
# ---------------------------- Database Production & Demo----------------------------
#
# production
db-create-revision-demo:  ## create alembic revision for production database
	alembic -c alembic-demo.ini revision --autogenerate -m "$(title)"

db-create-migration-demo:  ## create alembic database migrations in production
	alembic -c alembic-demo.ini upgrade head

#
# --------------------------- Formatting & Linting ---------------------------
#
check-format:
	black --check .

format-fix:
	black .

lint:
	mypy --explicit-package-bases --config-file  mypy.ini

#
# -------------------------------- Security -----------------------------------
#
create-admin-key:
	@PYTHONPATH=. python3 app/tools/my_cli.py

change-usdt-price:
	@PYTHONPATH=. python3 app/tools/change_price.py


#
# ------------------------ Digital Ocean Deployments ---------------------------
#
do-dev-start:  ## start dev deployment on digital ocean
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/dev.yml --profile dev up -d

do-demo-start:  ## start dev deployment on digital ocean
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/demo.yml --profile demo up -d

do-prd-start:  ## start production deployment on digital ocean
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/prd.yml --profile production up -d