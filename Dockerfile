FROM python:3.13
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

RUN apt-get update && apt-get install -y \
    libsasl2-dev \
    python3-dev \
    libldap2-dev \
    libssl-dev \
    libcairo2-dev \
    pango1.0-tests \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
 && rm -rf /var/lib/apt/lists/*

# Install pip modules
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app
