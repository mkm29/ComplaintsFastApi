# Dockerfile
## Build venv
FROM python:3.10 AS venv

ENV POETRY_VERSION=1.1.13
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# The `--copies` option tells `venv` to copy libs and binaries
# instead of using links (which could break since we will
# extract the virtualenv from this image)
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && pip install poetry && poetry install


## Beginning of runtime image
# Remember to use the same python version
# and the same base distro as the venv image
FROM python:3.10-alpine3.16 as prod

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY . ./

EXPOSE 5001

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:5001', timeout=2)"

ENTRYPOINT ["uvicorn"]
CMD ["--port", "5001", "main:app"]