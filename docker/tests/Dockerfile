FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY docker/tests/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-warn-script-location -r requirements.txt

RUN useradd -ms /bin/bash pythonuser
RUN mkdir -p /pytest_cache
RUN chown -R pythonuser:pythonuser /code /pytest_cache
USER pythonuser

COPY --chown=pythonuser:pythonuser ../../ /code

ENV PYTEST_CACHE_DIR=/pytest_cache

ENTRYPOINT ["python", "-m", "pytest"]