# KA Back-end

Here lies back-end source code for Karya Angkatan CSUI 2021.

## Requirements

-   Python >=3.7
-   Poetry
-   PostgresQL/MySQL (Any that is supported by SQLAlchemy is fine, but these two are the only one tested)

## Setup

-   Create a `.env` file with the following template

```
database_url =
secret       =
hostname     =
frontend_url = []
upload_path  =
sentry_url   = # Optional
redis_url    = # Optional
```

-   Install project with poetry

```
$ poetry install
```

-   Run database migration

```
$ poetry run alembic upgrade head
```

-   Run with `uvicorn`

```
$ poetry run uvicorn app:app
```
