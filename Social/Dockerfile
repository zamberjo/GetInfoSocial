FROM python:3.7-alpine as builder
WORKDIR /wheels
RUN apk add --no-cache \
    g++ \
    gcc \
    git \
    openssl-dev \
    python3-dev \
    libffi-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers
RUN pip wheel cython \
    python-telegram-bot && \
    git clone https://github.com/sherlock-project/sherlock.git && \
    pip wheel -r /wheels/sherlock/requirements.txt && \
    git clone https://github.com/sundowndev/PhoneInfoga

COPY phoneinfoga.config.py /wheels/PhoneInfoga/config.py

FROM python:3.7-alpine
WORKDIR /Social

COPY --from=builder /wheels /wheels
COPY --from=builder /wheels/sherlock /sherlock
COPY --from=builder /wheels/PhoneInfoga /PhoneInfoga

RUN pip install python-telegram-bot -f /wheels && \
    pip install -r /sherlock/requirements.txt -f /wheels && \
    pip install -r /PhoneInfoga/requirements.txt -f /wheels && \
    rm -rf /wheels && \
    rm -rf /root/.cache/pip/*

COPY . /Social
CMD [ "python", "-u", "./entrypoint.py" ]
