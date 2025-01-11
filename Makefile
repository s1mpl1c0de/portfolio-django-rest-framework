build:
	docker compose build

collectstatic:
	docker compose exec django python manage.py collectstatic

createsuperuser:
	docker compose exec django python manage.py createsuperuser

down:
	docker compose down

dumpdata:
	docker compose exec django python manage.py dumpdata --indent 4 accounts.UserProfile > \
	./backend/apps/accounts/fixtures/user_profile.json

flake8:
	cd backend && flake8

loaddata:
	docker compose exec django python manage.py loaddata user_profile.json

logs:
	docker compose logs --timestamps --follow django

migrations:
	docker compose exec django python manage.py makemigrations

migrate:
	docker compose exec django python manage.py migrate

up:
	docker compose up -d
