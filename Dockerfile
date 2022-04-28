FROM python:3.9-slim-buster

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

RUN pip install --no-warn-script-location -r requirements.txt

ADD . /code

ENTRYPOINT ["python", "main.py"]
