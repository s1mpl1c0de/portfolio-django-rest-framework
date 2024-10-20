build:
	docker compose build

collectstatic:
	docker compose exec backend python manage.py collectstatic

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

down:
	docker compose down

dumpdata:
	docker compose exec backend python manage.py dumpdata --indent 4 accounts.UserProfile > \
	./backend/apps/accounts/fixtures/user_profile.json

flake8:
	cd backend && flake8

migrations:
	docker compose exec backend python manage.py makemigrations

migrate:
	docker compose exec backend python manage.py migrate

up:
	docker compose up -d
