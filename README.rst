Study Case: Single Page Application + Python Backend
====================================================

The goal of this project is to develop the same web application using different but equivalent technologies.
The frontend will be a SPA_ build with Vue.js_ and another version with Svelte_.
The backend will be a basic data (REST/GraphQL) API.
There will be four different versions built with the Python web frameworks Quart_, FastAPI_, Tornado_ and Falcon_.


Requirements
============

This is a monorepo_ that contains several related subprojects.
To spin up the whole project, you will need:

* Docker_
* `Docker Compose`_
* Make_ as the building tool

To run each backend Python project individually:

* Python 3.8+
* Poetry_ as the package manager
* Make_

.. tip::

    Using :code:`Make` is not mandatory since you can run any of its tasks manually if you like.


Running the Composite Project
=============================

From the root of the project, execute::

    make run

And then, access the project from :code:`https://localhost/`.



.. _SPA: https://en.wikipedia.org/wiki/Single-page_application
.. _monorepo: https://en.wikipedia.org/wiki/Monorepo
.. _Vue.js: https://vuejs.org/
.. _Svelte: https://svelte.dev/
.. _Quart: https://pgjones.gitlab.io/quart/
.. _FastAPI: https://fastapi.tiangolo.com/
.. _Tornado: https://www.tornadoweb.org/en/stable/
.. _Falcon: https://github.com/falconry/falcon
.. _Docker: https://docs.docker.com/get-docker/
.. _Docker Compose: https://docs.docker.com/compose/install/
.. _Poetry: https://python-poetry.org/
.. _Make: https://en.wikipedia.org/wiki/Make_(software)
