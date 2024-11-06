.PHONY: flake, startproject

# commands to run linting
flake:
	@docker-compose run --rm app sh -c "flake8"

# commands to start a new project
startproject:
	@docker-compose run --rm app sh -c "django-admin startproject app ."

