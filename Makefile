# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


# DOCKER TASKS
start_db: ## Run a Postgres container on port 35432 and name store-db
	docker run --name complaints-db -d -p 15432:5432 -e POSTGRES_USER=complaints -e POSTGRES_PASSWORD=complaints -e POSTGRES_DB=complaints postgres:14.3-alpine3.16

stop_db: ## Stop the db container
	docker container stop complaints-db

server: ## Start the server
	uvicorn --reload --port 5001 app.main:app