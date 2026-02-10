DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_ENV = --env-file src/.env
APP_CONTAINER = coffee_shop_app

APP_FILE = docker_compose/app.yaml
POSTGRES_FILE = docker_compose/postgres.yaml
REDIS_FILE = docker_compose/redis.yaml
RABBITMQ_FILE = docker_compose/rabbitmq.yaml
ADMINER_FILE = docker_compose/adminer.yaml
VOLUMES_FILE = docker_compose/volumes.yaml

.PHONY: app
app:
	${DC} -f ${POSTGRES_FILE} -f ${APP_FILE} ${APP_ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: pg
pg:
	${DC} -f ${POSTGRES_FILE} -f ${VOLUMES_FILE} -f ${ADMINER_FILE} ${APP_ENV} up --build -d
.PHONY: pg-down
pg-down:
	${DC} -f ${POSTGRES_FILE} -f ${VOLUMES_FILE} -f ${ADMINER_FILE} down

.PHONY: redis
redis:
	${DC} -f ${REDIS_FILE} -f ${VOLUMES_FILE} ${APP_ENV} up -d
.PHONY: redis-down
redis-down:
	${DC} -f ${REDIS_FILE} -f ${VOLUMES_FILE} down

.PHONY: rabbitmq
rabbitmq:
	${DC} -f ${RABBITMQ_FILE} -f ${VOLUMES_FILE} ${APP_ENV} up -d

.PHONY: rabbitmq-down
rabbitmq-down:
	${DC} -f ${RABBITMQ_FILE} -f ${VOLUMES_FILE} down

.PHONY: all
all:
	${DC} -f docker_compose/compose.yaml ${APP_ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f docker_compose/compose.yaml down
