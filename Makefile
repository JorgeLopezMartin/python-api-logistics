include ./makefile_help.mk

.DEFAULT_GOAL := help

.PHONY: build
build: ##@development Build the containers.
	docker build -t python-api-jorge .

.PHONY: start
start: ##@development Run the containers required for the service to work.
start:
	docker-compose up -d server

.PHONY: clean
clean: ##@development Stop and remove the containers created by the start command.
	docker-compose down --remove-orphans --volumes

.PHONY: shell
shell: ##@development Start a bash shell in a container.
	docker-compose run --rm shell

.PHONY: logs
logs: ##@development Show logs for the current project.
	docker-compose logs -f

.PHONY: makemigrations
makemigrations: ##@database Run the command to autogenerate new migrations on the database for missing model changes. Set the name using msg=<migration_name>
makemigrations: msg?=''
makemigrations:
	docker-compose run migrations revision --auto -m "${msg}"

.PHONY: migrate
migrate: ##@database Apply migrations on running database container. You can specify the desired revision using revision=<migration_id>
migrate: revision?='head'
migrate:
	docker-compose run --rm migrations upgrade ${revision}

.PHONY: downgrade-db
downgrade-db: ##@database Downgrade the database to the previous version, or to the specified version with revision=<migration_id>
downgrade-db: revision?='-1'
downgrade-db:
	docker-compose run --rm migrations downgrade ${revision}


.PHONY: tests
tests: ##@test Run tests.
	docker-compose run --rm integration_test

.PHONY: integration-tests
integration-tests: ##@test Run integration tests
	docker-compose run --rm integration_test -m integration

.PHONY: pylint
pylint: ##@test Run pylint verification.
pylint: args ?= --rcfile=.pylintrc /code/app
pylint:
	docker-compose run --rm --no-deps pylint --ignore=tests ${args}