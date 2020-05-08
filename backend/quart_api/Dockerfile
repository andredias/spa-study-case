FROM python:3.8-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# hadolint ignore=DL3018
RUN apk --no-cache add build-base libffi-dev libxml2-dev libxslt-dev openssl openssl-dev bsd-compat-headers

RUN python -m venv /venv
ENV PATH=/venv/bin:${PATH}
RUN pip install --no-cache-dir dumb-init poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev



FROM python:3.8-alpine as final

COPY --chown=nobody:nobody --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
RUN chown -R nobody:nobody /app
COPY --chown=nobody:nobody app /app
COPY --chown=nobody:nobody cert /app/cert
COPY --chown=nobody:nobody hypercorn.toml .

USER nobody

EXPOSE 8080 8443
ENTRYPOINT ["dumb-init", "--"]
CMD ["hypercorn", "--config=hypercorn.toml", ".:create_app()"]