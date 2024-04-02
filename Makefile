.env:  ## Ensures that env file exists
	@cp -n .env.example .env

include ./app/.env
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
	make build-frontend


build-api:  ## build docker images
	echo "Building images"
	docker build -t wasata/api ./app

build-frontend:  ## build moamalat payment image
	echo "Building frontend"
	docker build -t wasata/frontend ./frontend

build-db:  ## build database image
	echo "Building database"
	docker build -t wasata/dev-postgres ./dev-database

dev-start-db:
	docker run wasata/dev-postgres

test-start:  ## build docker containers for dev environment
	set -a; source deploy/envs/dev.env; set +a; docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/dev.yml --profile dev up -d

demo-start:  ## build docker containers for demo environment
	set -a; source deploy/envs/demo.env; set +a; docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/demo.yml --profile demo up -d


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
db-create-revision:  ## create alembic revision for development database
	alembic -c alembic.ini revision --autogenerate -m "$(title)"

db-create-migration:  ## create alembic database migrations in development
	alembic -c alembic.ini upgrade head


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
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/dev.yml --profile dev up --build -d

do-demo-start:  ## start dev deployment on digital ocean
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/demo.yml --profile demo up -d

do-prd-start:  ## start production deployment on digital ocean
	docker compose -p $(docker-project-name) -f deploy/compose/common.yml -f deploy/compose/prd.yml --profile production up -d