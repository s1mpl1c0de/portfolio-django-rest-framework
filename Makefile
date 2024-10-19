build:
	docker compose build

collectstatic:
	docker compose exec backend python manage.py collectstatic

down:
	docker compose down

migrations:
	docker compose exec backend python manage.py makemigrations

migrate:
	docker compose exec backend python manage.py migrate

up:
	docker compose up -d
