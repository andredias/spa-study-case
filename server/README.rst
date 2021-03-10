Running services in development
===============================

In development, to debug the FastAPI, Tornado, etc project locally
you need Postgres and Redis running::

    $ docker-compose --env-file .env.dev up postgres redis

The `.env.dev` configures the network to `web`.
Thus `postgres` and `redis` are available at `localhost`.
