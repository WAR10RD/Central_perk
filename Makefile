ENV="dev"
HOST="db"

build_api:
	docker build -f deployment/docker/dockerfile -t central/api:latest .

build_cron_jobs:
	docker build -f deployment/docker/cronjob.dockerfile -t central/$(ENV)/cron_jobs:latest .

setup_env: build_api build_cron_jobs start migrations migrate

start:
	docker-compose -f deployment/docker/docker-compose.yml up -d

stop:
	docker-compose -f deployment/docker/docker-compose.yml down

logs:
	docker-compose -f deployment/docker/docker-compose.yml logs -f

live_shell:
	docker exec -it $$(docker ps --filter "name=^central_api$$" --format "{{.ID}}") /bin/bash

migrations:
	docker run --add-host=$(HOST):host-gateway \
 		--env-file $(ENV).env $$(docker image ls "central/api" --format "{{.ID}}") \
 		python /app/manage.py makemigrations

merge_migration:
	docker run --add-host=$(HOST):host-gateway \
 		--env-file $(ENV).env $$(docker image ls "central/api" --format "{{.ID}}") \
 		python /app/manage.py makemigrations --merge

showmigrations:
	docker run --add-host=$(HOST):host-gateway \
 		--env-file $(ENV).env $$(docker image ls "central/api" --format "{{.ID}}") \
 		python /app/manage.py showmigrations


migrate:
	docker run --add-host=$(HOST):host-gateway \
		--env-file $(ENV).env $$(docker image ls "central/api" --format "{{.ID}}") \
		 python /app/manage.py migrate

createsuperuser:
	sudo docker run --add-host=$(HOST):host-gateway \
 		--env-file $(ENV).env $$(docker image ls "central/api" --format "{{.ID}}") \
 		python /app/manage.py createsuperuser --email=admin@admin.com
