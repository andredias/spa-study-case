FROM python:3.8-slim

RUN python -m venv /venv
ENV PATH=/venv/bin:${PATH}
RUN pip install --no-cache-dir dumb-init poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

RUN chown -R nobody:nogroup /app
COPY --chown=nobody:nogroup app /app/app
COPY --chown=nobody:nogroup cert /app/cert
USER nobody

EXPOSE 8443
ENTRYPOINT ["dumb-init", "--"]
CMD ["python", "-m", "app.main"]
