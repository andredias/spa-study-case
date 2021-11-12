FROM python:3.11.0a2-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk --no-cache add build-base libffi-dev libxml2-dev libxslt-dev openssl openssl-dev bsd-compat-headers curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

RUN python -m venv /venv
ENV PATH=/venv/bin:/root/.poetry/bin:${PATH}
RUN pip install --upgrade pip && pip install dumb-init

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev



FROM python:3.11.0a2-alpine as final

RUN apk --no-cache add libstdc++

COPY --chown=nobody:nogroup --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
RUN chown -R nobody:nogroup /app
COPY --chown=nobody:nogroup app /app
COPY --chown=nobody:nogroup hypercorn.toml .

USER nobody

EXPOSE 8443
ENTRYPOINT ["dumb-init", "--"]
CMD ["hypercorn", "--config=hypercorn.toml", ".:create_app()"]
