# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

### Install dependencies
RUN apk update && \
    apk add --no-cache \
        apache2-utils \
        curl \
        git \
        libffi \
        tzdata \
        python3 && \
    ln -sf python3 /usr/bin/python && \
    apk add --no-cache --virtual .build-dependencies \
        gcc \
        musl-dev \
        libffi-dev \
        python3-dev \
        py3-pip && \
    python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir \
        radicale \
        passlib[bcrypt] \
        bcrypt \
        defusedxml && \
    apk del --purge .build-dependencies && \
    rm -rf /var/cache/apk/* /tmp/* /root/.cache

ENV PATH="/opt/venv/bin:$PATH"

### Add metadata
LABEL org.opencontainers.image.authors="dale.stirling@gmail.com"
LABEL org.opencontainers.image.vendor="dalethestirling"

### Copy root filesystem
COPY rootfs /
