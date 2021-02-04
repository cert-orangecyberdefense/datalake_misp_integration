FROM python:3.8-slim-buster

# System deps:
RUN apt-get update \
  && apt-get install -y \
    gcc \
    libfuzzy-dev \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash pythonuser
USER pythonuser

WORKDIR /code

ADD ./requirements.txt /code/requirements.txt

# TODO Remove once pushed on the official pypi
RUN pip install -i https://test.pypi.org/simple/  --no-warn-script-location datalake-scripts==1.23a0

RUN pip install --no-warn-script-location -r requirements.txt

ADD . /code

ENTRYPOINT ["python", "main.py"]
