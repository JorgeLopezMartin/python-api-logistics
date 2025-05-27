# python-api
A FastAPI python project with all necessary components

## Running the service:
In order to retrieve the available make commands, run `make help`.

The service can be run locally by executing `make build start`.

![Start](images/1_start.png)

Once the service is running, it can be accessed in the URL `http://127.0.0.1:8000` (i.e. `http://127.0.0.1:8000/ping`).

In order to ready the table entities, the database has to be *migrated*. To do so, execute `make migrate`.

![Migrate](images/2_migrate.png)

The tests can be run by executing `make tests`.

![Tests](images/3_tests.png)

Linter can be run by executing `make lint`.

![Lint](images/4_lint.png)

Logs can be shown in the terminal by running `make logs`.

A shell terminal inside the docker instance can be started by running `make shell`. To test python code, just run `python` once inside the shell terminal. The docker image will contain all the dependencies used in the service.

To stop and clean the containers, run `make clean`.

## Endpoints and usage:

The service automatically generates a `/docs` endpoint where all the endpoints are defined:

![Docs](images/5_endpoints.png)

### Location:

Defines a place where the cargoes can be located or destined to.

Create location:
```
POST /location

Request body (example):
{
  "data": {
    "name": "string",
    "latitude": 0,
    "longitude": 0
  }
}

Responses:

201: Successful response
Response body (example):
{
  "data": {
    "id": 0,
    "name": "string",
    "latitude": 0,
    "longitude": 0
  }
}

422: Validation error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
```

List locations
```
GET /location
Query params:
- name: str
- page: int
- page_size: int

Responses:

200: Successful response
Response body (example):
{
  "data": [
    {
      "id": 0,
      "name": "string",
      "latitude": 0,
      "longitude": 0
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find location:
```
GET /location/{location_id}

Responses:

200: Successful response
Response body (example):
{
  "data": {
    "id": 0,
    "name": "string",
    "latitude": 0,
    "longitude": 0
  }
}

404: Location not found
{
  "detail": [
    {
      "msg": "Location - Location not found",
      "type": "location_not_found"
    }
  ]
}
```

Delete location:
```
DELETE /location/{location_id}

Responses:

204: Successful response

404: Location not found
{
  "detail": [
    {
      "msg": "Location - Location not found",
      "type": "location_not_found"
    }
  ]
}

409: Location not deletable
{
  "detail": [
    {
      "msg": "Location - Location not deletable",
      "type": "location_not_deletable"
    }
  ]
}
```

Update location:
```
PATCH /location/{location_id}

Request body (example):
{
  "data": {
    "name": "string",
    "latitude": 0,
    "longitude": 0
  }
}

Responses:

204: Successful response

404: Location not found
{
  "detail": [
    {
      "msg": "Location - Location not found",
      "type": "location_not_found"
    }
  ]
}
```

### Client:

Defines each of the company's clients. A client can have more than one contract.

Create client:
```
POST /client

Request body(example):
{
  "data": {
    "name": "string"
  }
}

Responses:

201: Successful response
Response body (example):
{
  "data": {
    "id": 0,
    "name": "string"
  }
}

422: Validation error
Response body (example):
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

List clients:
```
GET /client
Query params:
- name
- page
- page_size

Responses:

200: Successful response
Response body (example):
{
  "data": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find client:
```
GET /client/{client_id}

Responses:

200: Successful response
{
  "data": {
    "id": 0,
    "name": "string"
  }
}

404: Client not found
{
  "detail": [
    {
      "msg": "Client - Client not found",
      "type": "client_not_found"
    }
  ]
}
```

Delete client:
```
DELETE /client/{client_id}

Responses:

204: Successful response

404: Client not found
{
  "detail": [
    {
      "msg": "Client - Client not found",
      "type": "client_not_found"
    }
  ]
}

409: Client cannot be deleted
{
  "detail": [
    {
      "msg": "Client - Client cannot be deleted",
      "type": "client_not_deletable"
    }
  ]
}
```

Update client
```
PATCH /client/{client_id}
Request body (example):
{
  "data": {
    "name": "string"
  }
}

Responses:

204: Successful response

404: Client not found
{
  "detail": [
    {
      "msg": "Client - Client not found",
      "type": "client_not_found"
    }
  ]
}
```

### Contract:

Each of the contracts a client has. It has a set of cargoes and a destionation location.

Create contract:
```
POST /contract
Request body (example):
{
  "data": {
    "price": 0,
    "client_id": 0,
    "location_id": 0
  }
}

Responses:

204: Successful response
Response body (example):
{
  "data": {
    "id": 0,
    "price": 0,
    "client_id": 0,
    "location_id": 0
  }
}

404: Client not found
{
  "detail": [
    {
      "msg": "Client - Client not found",
      "type": "client_not_found"
    }
  ]
}

404: Location not found
{
  "detail": [
    {
      "msg": "Location - Location not found",
      "type": "location_not_found"
    }
  ]
}

422: Validation error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

List contracts:
```
GET /contract
Query params:
- client_id
- location_id
- page
- page_size

Responses:

200: Successful response
Response body (example): 
{
  "data": [
    {
      "id": 0,
      "price": 0,
      "client_id": 0,
      "location_id": 0
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find contract:
```
GET /contract/{contract_id}

Responses:

200: Successful response
Response body (example):
{
  "data": {
    "id": 0,
    "price": 0,
    "client_id": 0,
    "location_id": 0
  }
}

404: Contract not found
{
  "detail": [
    {
      "msg": "Contract - Contract not found",
      "type": "contract_not_found"
    }
  ]
}
```

Delete contract:
```
DELETE /contract/{contract_id}

Responses:

200: Successful response

404: Contract not found
{
  "detail": [
    {
      "msg": "Contract - Contract not found",
      "type": "contract_not_found"
    }
  ]
}

409: Contract cannot be deleted
{
  "detail": [
    {
      "msg": "Contract - Contract not deletable",
      "type": "contract_not_deletable"
    }
  ]
}
```

Update contract:
```
PATCH /contract/{contract_id}
Request body (example):
{
  "data": {
    "price": 0
  }
}

Responses:

204: Successful response

404: Contract not found
{
  "detail": [
    {
      "msg": "Contract - Contract not found",
      "type": "contract_not_found"
    }
  ]
}
```

### Cargo:

Each cargo from a contract.

Create cargo:
```
POST /cargo

Request body (example):
{
  "data": {
    "type": 0,
    "quantity": 0,
    "contract_id": 0
  }
}

Responses:

201: Successful
Response body (example):
{
  "data": {
    "id": 0,
    "type": 0,
    "status": 0,
    "contract_id": 0
  }
}

404: Contract Not found
{
  "detail": [
    {
      "msg": "Contract - Contract not found",
      "type": "contract_not_found"
    }
  ]
}

422: Validation error
	

Validation Error
Media type

{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

List cargoes:
```
GET /cargo
Query params:
- type: int (0,1,2)
- status: int (0,1,2)
- contract_id: int
- page: int
- page_size: int

Responses:

200: Successful
{
  "data": [
    {
      "id": 0,
      "type": 0,
      "status": 0,
      "contract_id": 0
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find cargo:
```
GET /cargo/{cargo_id}

Responses:

200: Successful
{
  "data": {
    "id": 0,
    "type": 0,
    "status": 0,
    "contract_id": 0
  }
}

404: Cargo not found:
{
  "detail": [
    {
      "msg": "Cargo - Cargo not found",
      "type": "cargo_not_found"
    }
  ]
}
```

Delete cargo:
```
DELETE /cargo/{cargo_id}

Responses:

204: Successful response

404: Cargo not found
{
  "detail": [
    {
      "msg": "Cargo - Cargo not found",
      "type": "cargo_not_found"
    }
  ]
}

409: Cargo not deletable
{
  "detail": [
    {
      "msg": "Cargo - Cargo cannot be deleted",
      "type": "cargo_not_deletable"
    }
  ]
}
```

Update cargo:
```
PATCH /cargo/{cargo_id}
Request body:
{
  "data": {
    "type": 0,
    "quantity": 0
  }
}

Responses:

204: Successful

404: Cargo not found
{
  "detail": [
    {
      "msg": "Cargo - Cargo not found",
      "type": "cargo_not_found"
    }
  ]
}
```

### Vessel:

The entities that transport cargoes.

Create vessel:
```
POST /vessel
Request body:
{
  "data": {
    "name": "string",
    "capacity": 0
  }
}

Responses:

201: Successful
{
  "data": {
    "id": 0,
    "name": "string",
    "capacity": 0
  }
}

422: Validation error:
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

List vessels:
```
GET /vessel
Query params:
- name: str
- capacity: float
- page: int
- page_size: int

Responses:

200: Successful
{
   "data": [
    {
      "id": 0,
      "name": "string",
      "capacity": 0
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find vessel:
```
GET /vessel/{vessel_id}

Responses:

200: Successful
{
  "data": {
    "id": 0,
    "name": "string",
    "capacity": 0
  }
}

404: Vessel not found
{
  "detail": [
    {
      "msg": "Vessel - Vessel not found",
      "type": "vessel_not_found"
    }
  ]
}
```

Delete vessel:
```
DELETE /vessel/{vessel_id}

Responses:

204: Successful

404: Vessel not found
{
  "detail": [
    {
      "msg": "Vessel - Vessel not found",
      "type": "vessel_not_found"
    }
  ]
}
```

Update vessel:
```
PATCH /vessel/{vessel_id}
{
  "data": {
    "name": "string",
    "capacity": 0
  }
}

Responses:

204: Successful

404: Vessel not found
{
  "detail": [
    {
      "msg": "Vessel - Vessel not found",
      "type": "vessel_not_found"
    }
  ]
}
```

### Track:

Each piece of tracking information between cargoes and vessels. It is used to follow any cargo or vessel and know where they are in a specific moment in time. Tracks can have empty cargoes for empty vessel tracking.

When a cargo is pending, the first track instance changes the cargo status to in_transit. Once a track with the cargo in the contract's destination is created, the status of the cargo is changed to delivered.

If a cargo is moved after being delivered, an exception is raised.

Create track:
```
POST /track
{
  "data": {
    "date": "2025-05-27T18:31:01.003Z",
    "location_id": 0,
    "cargo_id": 0,
    "vessel_id": 0
  }
}

Responses:

201: Successful
{
  "data": {
    "id": 0,
    "date": "2025-05-27T18:31:01.004Z",
    "location_id": 0,
    "cargo_id": 0,
    "vessel_id": 0
  }
}

404: Cargo not found
{
  "detail": [
    {
      "msg": "Cargo - Cargo not found",
      "type": "cargo_not_found"
    }
  ]
}

404: Vessel not found
{
  "detail": [
    {
      "msg": "Vessel - Vessel not found",
      "type": "vessel_not_found"
    }
  ]
}

404: Location not found
{
  "detail": [
    {
      "msg": "Location - Location not found",
      "type": "location_not_found"
    }
  ]
}

409: Cargo already delivered
{
  "detail": [
    {
      "msg": "Cargo - Already delivered",
      "type": "cargo_already_delivered"
    }
  ]
}
```

List tracks:
```
GET /track
Query params:
- location_id: int
- cargo_id: int
- vessel_id: int
- page: int
- page_size: int

Responses:

200: Successful
{
  "data": [
    {
      "id": 0,
      "date": "2025-05-27T18:36:50.722Z",
      "location_id": 0,
      "cargo_id": 0,
      "vessel_id": 0
    }
  ],
  "pagination": {
    "page": 0,
    "page_size": 0,
    "total": 0
  }
}
```

Find track:
```
GET /track/{track_id}

Responses:

200: Successful
{
  "data": {
    "id": 0,
    "date": "2025-05-27T18:37:38.661Z",
    "location_id": 0,
    "cargo_id": 0,
    "vessel_id": 0
  }
}

404: Track not found
{
  "detail": [
    {
      "msg": "Track - Track not found",
      "type": "track_not_found"
    }
  ]
}
```

Delete track:
```
DELETE /track/{track_id}

Responses:

204: Successful

404: Track not found
{
  "detail": [
    {
      "msg": "Track - Track not found",
      "type": "track_not_found"
    }
  ]
}

409: Track cannot be deleted
{
  "detail": [
    {
      "msg": "Track - Track not deletable",
      "type": "track_not_deletable"
    }
  ]
}
```

Update track:
```
PATCH /track/{track_id}
{
  "data": {
    "date": "2025-05-27T18:39:33.900Z"
  }
}

Responses:

204: Successful

404: Track not found
{
  "detail": [
    {
      "msg": "Track - Track not found",
      "type": "track_not_found"
    }
  ]
}
```

### Implementation details:

- Client and Location entities added as they are going to be reused frecuently.
- DB Session middleware ensures each request done in a different transaction.
- View error handling function defined to be able to modify the way exceptions are handled accross the whole service.
- Repository, Service and View layers separate the different parts of the implementations (DB, business logic, request handling) to increase modularity.
- Base repository class ensures all entities handle database operations the same way.
- Linter and tests executed using in instances through make commands to easily apply them in pipelines.
- Database entities are automatically assigned creation date and modification date to track changes.
- Tracks can have Cargoes undefined to allow for tracking empty vessel locations.
- All API request and response schema signatures have been defined to ensure API contracts are consistent.

## Database:

Database configuration resides in the Docker-compose file. Running the service (`make start`) will also run the database. Database connection using the command line can be achieved with the `psql` tool by running `psql postgresql://postgres:password@0.0.0.0:5432/postgres`.

### Migrations:

Database migrations in this project are handled by alembic.

In order to generate the migration files of the new model changes, make sure the database is running and run `make makemigrations`. This will generate the necessary alembic migration files under `alembic/versions`.

To apply the migrations, run `make migrate`.

You can also downgrade migrations by running `make downgrade-db revision=<migration_id>` and migrate to a specific forward version with `make migrate revision=<migration_id>`. The migration_ids can be found in the alembic migration files.
