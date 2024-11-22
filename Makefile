.PHONY: flake, startproject, test, migrate, createsuperuser

# commands to run linting
flake:
	@docker-compose run --rm app sh -c "flake8"

# commands to start a new project
startproject:
	@docker-compose run --rm app sh -c "django-admin startproject app ."

# commands to run tests
test:
	@docker-compose run --rm app sh -c "python manage.py test"

# commands to run migrations
migrate:
	@docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"  

# commands to create superuser
createsuperuser:
	@docker-compose run --rm app sh -c "python manage.py createsuperuser"
