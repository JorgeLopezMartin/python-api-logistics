# python-api
A FastAPI python project with all necessary components

## Running the service:
In order to retrieve the available make commands, run `make help`.

The service can be run locally by executing `make build start`.

Once the service is running, it can be accessed in the URL `http://127.0.0.1:8000` (i.e. `http://127.0.0.1:8000/ping`).

A shell terminal inside the docker instance can be started by running `make shell`. To test python code, just run `python` once inside the shell terminal. The docker image will contain all the dependencies used in the service.

To stop and clean the containers, run `make clean`.

## Database:

Database configuration resides in the Docker-compose file. Running the service (`make start`) will also run the database. Database connection using the command line can be achieved with the `psql` tool by running `psql postgresql://postgres:password@0.0.0.0:5432/postgres`.

### Migrations:

Database migrations in this project are handled by alembic.

In order to generate the migration files of the new model changes, make sure the database is running and run `make makemigrations`. This will generate the necessary alembic migration files under `alembic/versions`.

To apply the migrations, run `make migrate`.

You can also downgrade migrations by running `make downgrade-db revision=<migration_id>` and migrate to a specific forward version with `make migrate revision=<migration_id>`. The migration_ids can be found in the alembic migration files.