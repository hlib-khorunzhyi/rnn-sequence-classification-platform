FROM python:3.12-slim

ARG USER_ID
ARG USER_NAME

ENV USER_NAME=${USER_NAME:-defaultuser} \
    USER_ID=${USER_ID:-1000}

ENV HOME=/home/${USER_NAME} \
    VIRTUAL_ENV=/home/${USER_NAME}/venv 

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Warsaw \
    PATH="/usr/local/gcloud/google-cloud-sdk/bin:${VIRTUAL_ENV}/bin:${HOME}/.local/bin:${PATH}" \
    PYTHONPATH=/app \
    BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim gcc curl git build-essential libb64-dev ca-certificates gnupg \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fSL https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-489.0.0-linux-x86_64.tar.gz -o /tmp/google-cloud-sdk.tar.gz \
    && mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xzf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --quiet \
    && rm /tmp/google-cloud-sdk.tar.gz

RUN addgroup --system --gid ${USER_ID} ${USER_NAME} \
    && useradd --system -m --no-log-init --home-dir ${HOME} --uid ${USER_ID} --gid ${USER_NAME} --group ${USER_NAME} ${USER_NAME}

RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}
RUN mkdir -p /app && chown -R ${USER_NAME}:${USER_NAME} /app /tmp

RUN curl -sSL https://install.python-poetry.org | HOME=${HOME} python3 - \
    && chown -R ${USER_NAME}:${USER_NAME} ${HOME}/.local

USER ${USER_NAME}

COPY pyproject.toml *.lock /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
    && python3.12 -m venv ${VIRTUAL_ENV} \
    && pip install --upgrade pip setuptools \
    && poetry install && cp poetry.lock ${BUILD_POETRY_LOCK} \
    && rm -rf ${HOME}/.cache/*

USER root
COPY ./docker/scripts/* /
RUN chown -R ${USER_NAME} /*.sh && chmod +x /*.sh
USER ${USER_NAME}

COPY . /app/
CMD ["/startup-script.sh"]

RUN git config --global user.email "khorunzhyi519@gmail.com" \
    && git config --global user.name "Hlib Khorunzhyi"