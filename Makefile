build:
	docker compose build

collectstatic:
	docker compose exec backend python manage.py collectstatic

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

down:
	docker compose down

migrations:
	docker compose exec backend python manage.py makemigrations

migrate:
	docker compose exec backend python manage.py migrate

up:
	docker compose up -d
