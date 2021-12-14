MAIN_SERVICE = app_api
MANAGE_PY = /app/myproject/manage.py

format:
	autoflake --remove-unused-variables --ignore-init-module-imports --remove-all-unused-imports -i -r .
	isort .
	python3 -m black -l 100 .

migrate:
	docker-compose exec $(MAIN_SERVICE) python3 $(MANAGE_PY) migrate


makemigrations:
	docker-compose exec $(MAIN_SERVICE) python3 $(MANAGE_PY) makemigrations

ps:
	docker-compose ps

up:
	docker-compose up -d
	docker-compose ps

down:
	docker-compose down

run:
	docker-compose build --parallel --no-cache
	docker-compose up -d
	docker-compose ps

rebuild:
	docker-compose build --parallel
	docker-compose up -d
	docker-compose ps

restart:
	docker-compose restart $(MAIN_SERVICE)
	docker-compose ps

run_tests:
	docker-compose exec $(MAIN_SERVICE) python3 $(MANAGE_PY) test
