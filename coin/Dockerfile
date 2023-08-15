
FROM --platform=linux/amd64 python:3-alpine as dependency_exporter
ENV PYTHONUNBUFFERED=true
WORKDIR /app
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN poetry export -f requirements.txt --output ./requirements.txt --without-hashes

FROM --platform=$TARGETPLATFORM python:3-slim as dependency_loader
ENV PYTHONUNBUFFERED=true
WORKDIR /app

COPY --from=dependency_exporter /app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --target=./libraries --no-dependencies

FROM --platform=$TARGETPLATFORM python:3-slim as runtime
ENV PYTHONUNBUFFERED=true
WORKDIR /app

COPY --from=dependency_loader /app/libraries /app/libraries
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/libraries"


ENV PYTHONPATH="${PYTHONPATH}:/app"
COPY coin_server /app/coin_server

EXPOSE 7979

ENTRYPOINT ["python3", "-u", "coin_server/__main__.py"]