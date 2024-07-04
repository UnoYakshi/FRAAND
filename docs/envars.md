This is the list of environment variables you need to work with the FRAAND project.
In brackets `( <value> )` you will find the working values for development,
i.e., they are good to go with [docker-compose.dev.yml](../docker-compose.dev.yml).


# FRAAND Core

## PostgreSQL Database
- `POSTGRES_HOST` (`localhost`) — DB server address, can be docker-compose hostnames.
- `POSTGRES_PORT` (`5432`) — DB server port.
- `POSTGRES_USER` (`fraand_user`) — DB user, don't use `postgres` or `root`!
- `POSTGRES_PASSWORD` — DB user password, use complex generated passwords only!
- `POSTGRES_DB` (`fraand_db`) — actual database name/address in the DBMS.

## Cross-origin resource sharing ([CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS))
TODO: Explain this section, fix `[*]`...
- `CORS_CREDENTIALS` (`True`)
- `CORS_ORIGINS` (`[*]`)
- `CORS_METHODS` (`[*]`)
- `CORS_HEADERS` (`[*]`)

## FastAPI
- `FASTAPI_ENV` (`DEV`) — used to determine whether to generate OpenAPI (`/docs` route).
- `ENVIRONMENT` (`dev`) — used in [Dockerfile](../Dockerfile) to determine correct requirements file (in `requirements/` folder).
- `TITLE` (`FRAAND`) — project's title to display in OpenAPI, etc.
- `PATH_TO_PROJECT` — an absolute path to your project's root directory, used in `docker-compose*.yml` for mounting volumes correctly.

## General
- `DEBUG` — general debug mode for multiple modules (?)
- `CADDY_INGRESS_NETWORKS` — will likely help auto-discovery for [caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy) (set it to `caddy`).
