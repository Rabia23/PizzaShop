install-requirements:  ## install application requirements
	pip install -r requirements.txt

start-server: ## run django application on specific port
	python manage.py runserver 8000

tests: ## run all unittests
	python manage.py test --keepdb

init-db: ## import data into database from csv file
	python manage.py init_db

showmigrations: ## show database migrations
	python manage.py showmigrations

makemigrations: ## make database migrations
	python manage.py makemigrations

migrate: ## push migrations into the database
	python manage.py migrate

django-tests: ## run all unittests inside docker
	docker-compose run django python manage.py test --keepdb

django-migrate: ## push migrations into the database inside docker
	docker-compose run django python manage.py migrate

buildup: ## build and up all the services
	docker-compose up --build

up: ## up all the services
	docker-compose up

start: ## start all the services
	docker-compose start

restart: ## restart all the services
	docker-compose restart

stop: ## stop all the services
	docker-compose stop

django-shell: ## open django service bash shell
	docker exec -it signicat_app bash

db-shell: ## open db service bash shell
	docker exec -it signicat_db bash

shell: ## open django shell
	docker-compose run django python manage.py shell

create-superuser: ## create super user for django admin
	python manage.py createsuperuser

create-drf-token: ## create drf token for api's authentication
	python manage.py drf_create_token -r <username>