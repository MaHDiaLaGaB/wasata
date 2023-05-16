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


images:  ##  Build all images
	echo "Building images"
	cd dev-database && make image-db
	make image-api


image-api:  ## build docker images
	echo "Building images"
	docker build -t wasata/api .

build-up:  ## build docker containers
	docker-compose -f docker-compose.yml up -d


down:  ## stop the active docker containers
	docker-compose down



db-create-revision:  ## create alembic revision for database
	alembic revision --autogenerate -m "$(title)"

db-create-migration:  ## create alembic database migrations
	alembic --name alembic upgrade head


check-format:
	black --check .

format-fix:
	black .