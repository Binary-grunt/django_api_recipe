.PHONY: flake, startproject, test

# commands to run linting
flake:
	@docker-compose run --rm app sh -c "flake8"

# commands to start a new project
startproject:
	@docker-compose run --rm app sh -c "django-admin startproject app ."

test:
	@docker-compose run --rm app sh -c "python manage.py test"
