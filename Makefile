# Make all targets .PHONY
.PHONY: $(shell sed -n -e ' /^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

SHELL = /usr/bin/env bash
USER_NAME = $(shell whoami)
USER_ID = $(shell id -u)
HOST_NAME = $(shell hostname)


ifeq (, $(shell docker compose version 2>/dev/null))
	DOCKER_COMPOSE_COMMAND = docker-compose
else
	DOCKER_COMPOSE_COMMAND = docker compose
endif

SERVICE_NAME = app
CONTAINER_NAME = rnn-sequence-classification-platform-container

DIRS_TO_VALIDATE = src
DOCKER_COMPOSE_RUN = $(DOCKER_COMPOSE_COMMAND) run --rm $(SERVICE_NAME)
DOCKER_COMPOSE_EXEC = $(DOCKER_COMPOSE_COMMAND) exec $(SERVICE_NAME)

LOCAL_DOCKER_IMAGE_NAME = rnn-sequence-classification-platform
GCP_DOCKER_IMAGE_NAME = europe-west4-docker.pkg.dev/project-6b154f17-21bb-4de7-947/rnn-sequence-classification-platform/data-processing
GCP_DOCKER_IMAGE_TAG := $(shell uuidgen)

export SSH_AUTH_SOCK
export

# Returns true if the stem is a non-empty environment variable, or else raises an error
guard-%:
	@#$(or ${$*}, $(error $* is no set))

## Generate final config. CONFIG_NAME=<config_name> has to be provided for overrides use: OVERRIDES=<overrides>
generate-final-config: up guard-CONFIG_NAME
	$(DOCKER_COMPOSE_EXEC) python ./src/generate_final_config.py --config-name $(CONFIG_NAME) --overrides process_data.docker_image_name=$(GCP_DOCKER_IMAGE_NAME) process_data.docker_image_tag=$(GCP_DOCKER_IMAGE_TAG) $(OVERRIDES)

## Generate final main config.
generate-main-config: up
	$(DOCKER_COMPOSE_EXEC) python ./src/generate_final_config.py --config-name config --overrides process_data.docker_image_name=$(GCP_DOCKER_IMAGE_NAME) process_data.docker_image_tag=$(GCP_DOCKER_IMAGE_TAG) $(OVERRIDES)

## Version data
version-data: up
	$(DOCKER_COMPOSE_EXEC) python ./src/version_data.py

## Processes raw data
process-data: generate-main-config push
	$(DOCKER_COMPOSE_EXEC) python ./src/process_data.py

## Local processes raw data
local-process-data: generate-main-config
	$(DOCKER_COMPOSE_EXEC) python ./src/process_data.py --config_name config --overrides process_data.docker_image_name=$(GCP_DOCKER_IMAGE_NAME) process_data.docker_image_tag=$(GCP_DOCKER_IMAGE_TAG)

## Push docker image to GCP artifact registery
push: build
	gcloud auth configure-docker --quiet europe-west4-docker.pkg.dev
	docker tag $(LOCAL_DOCKER_IMAGE_NAME):latest "$(GCP_DOCKER_IMAGE_NAME):$(GCP_DOCKER_IMAGE_TAG)"
	docker push "$(GCP_DOCKER_IMAGE_NAME):$(GCP_DOCKER_IMAGE_TAG)"

## Prepare dataset
prepare-dataset: up
	$(DOCKER_COMPOSE_EXEC) python ./src/prepare_data.py

## Starts jupyter lab
notebook: up
	$(DOCKER_COMPOSE_EXEC) jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser

## Sort code using isort
sort: up
	$(DOCKER_COMPOSE_EXEC) isort --atomic $(DIRS_TO_VALIDATE)

## Check sorting using isort
sort-check: up
	$(DOCKER_COMPOSE_EXEC) isort --check-only --atomic $(DIRS_TO_VALIDATE)

## Format code using black
format: up
	$(DOCKER_COMPOSE_EXEC) black $(DIRS_TO_VALIDATE)

## Check format using black
format-check: up
	$(DOCKER_COMPOSE_EXEC) black --check $(DIRS_TO_VALIDATE)

## Format and sort code using black and isort
format-and-sort: sort format

## Lint code using flake8
lint: up format-check sort-check
	$(DOCKER_COMPOSE_EXEC) flake8 $(DIRS_TO_VALIDATE)

## Check type annotations using mypy
check-type-annotations: up
	$(DOCKER_COMPOSE_EXEC) mypy $(DIRS_TO_VALIDATE)
# 	$(DOCKER_COMPOSE_EXEC) mypy --clean-cache $(DIRS_TO_VALIDATE)

## Run tests with pytest
test: up
	$(DOCKER_COMPOSE_EXEC) pytest

## Perform a full check
full-check: lint check-type-annotations
	$(DOCKER_COMPOSE_EXEC) pytesta --cov --cov-report xml --verbose

## Builds docker image
build:
	$(DOCKER_COMPOSE_COMMAND) build $(SERVICE_NAME)

## Remove poetry.lock and build docker image
build-for-dependencies:
	rm -f *.lock
	$(DOCKER_COMPOSE_COMMAND) build $(SERVICE_NAME)

## Lock dependencies with poetry
lock-dependencies: build-for-dependencies
	$(DOCKER_COMPOSE_RUN) bash -c "if [ -e /home/${USER_NAME}/poetry.lock.build ]; then cp /home/${USER_NAME}/poetry.lock.build ./poetry.lock; else poetry lock; fi"

## Starts docker container using "docker-compose up -d"
up:
	$(DOCKER_COMPOSE_COMMAND) up -d

## docker-compose down
down:
	$(DOCKER_COMPOSE_COMMAND) down

## Open an interactive shell in docker container
exec-in: up
	docker exec -it $(CONTAINER_NAME) bash


