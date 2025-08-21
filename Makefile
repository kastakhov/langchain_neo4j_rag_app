PROJECT_NAME := ai-bot
TARGET := $(firstword $(MAKECMDGOALS))
CONTAINER_NAME := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
DOCKER = $(shell docker 2>/dev/null >/dev/null && echo docker || exit 1) 
COMPOSE = $(shell docker compose version 2>/dev/null >/dev/null && echo docker compose || echo docker-compose)
COMPOSE_FILE := docker-compose-dev.yml

build: 
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) build $(CONTAINER_NAME)

start:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d $(CONTAINER_NAME)

stop:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) stop $(CONTAINER_NAME)

down:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down $(CONTAINER_NAME)

destroy:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down -v $(CONTAINER_NAME)

ps:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) ps

stats:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) stats

login:
ifdef CONTAINER_NAME
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -it $(CONTAINER_NAME) /bin/bash
else
	@echo "CONTAINER_NAME is not set" && exit 1
endif

rebuild: destroy clean build start

rebuild-api:
	$(MAKE) rebuild chatbot_api

rebuild-frontend:
	$(MAKE) rebuild chatbot_frontend

restart: stop start

logs:
	$(COMPOSE) -f $(COMPOSE_FILE) -p $(PROJECT_NAME) logs -f $(CONTAINER_NAME)

clean:
	find . -type f -not -path "./venv/*" -name '*.py[co]' -delete
	find . -type d -not -path "./venv/*" -name __pycache__ -exec rm -rf {} \; || true

%::
	@true
