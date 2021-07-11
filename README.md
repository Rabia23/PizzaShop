### Summary:

The application is a pizza shop, in which you can create, fetch, update and delete pizza orders. Only authenticated users are allowed to make calls. 

The REST APIs are built using Python Django framework and Mysql database.

### Project Structure (App Based):
```bash
PIZZASHOP/
├── README.md
├── hours.txt
├── pizzashop
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── .gitignore
│   ├── manage.py
│   ├── requirements.txt
│   ├── apps
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── management
│   │   │   │   └── commands
│   │   │   │       ├── __init__db
│   │   │   │       ├── init_db.py
│   │   │   │       └── wait_for_db.py
│   │   │   ├── migrations
│   │   │   │   ├── 0001_initial.py
│   │   │   │   └── __init__.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── tests
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_views.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   └── pagination.py
│   ├── conf
│   │   └── init.sql
│   ├── data
│   │   └── dataset.csv
│   ├── pizzashop
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
├── pyproject.toml
└── tox.ini
```

### Python Libraries/Frameworks used:
-  **django** - This is a Python-based open-source web framework that follows the model-template-view
architectural pattern.
-  **djangorestframework** - This is a powerful and flexible toolkit built on top of the Django web framework
for building REST APIs.
-  **mysqlclient** - MySQL database connector for Python.
-  **drf-yasg** - This is a Swagger generation tool provided by Django Rest Framework that allow you
to build API documentation.
-  **black** - This is Python code formatter that formats code adhering to PEP8 standards.

### How to get the application up and running using docker

This setup uses [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/) to provide a reproducible and easy to use environment.

Just run ```make buildup``` to get it started.
The app will bind to port 8000 and the mysql database will bind to port 3306 so please make sure the ports are not already in use. Stop all other containers or servers to be sure. It will also create the mysql database and tables for you.

Run ```make django-tests``` to execute the tests.

### How to get the application up and running using virtual environment

This setup will install everything inside the virtual environment and requires bit more steps than docker to perform to get the application started.

Before started, make sure Mysql is installed and running in your system.

Create and activate the virtual environment using commands ```python3 -m venv env``` and ```source env/bin/activate```.

Login into mysql server and run the sql script `source /Users/rabia/Downloads/PizzaShop/pizzashop/conf/init.sql` to create database. (absolute path to init.sql file)

Once database is created, do the three steps:
- Install project requirements:  ```make install-requirements```
- Create database tables:  ```make migrate```
- Run the application server:  ```make start-server```

Run ```make tests``` to execute the tests.


### How to get authentication token to access the APIs
Run the command ```make create-superuser``` to create the application user and get the token for that user by running command ```python manage.py drf_create_token -r <username>```


Once everything is built and running with either of the setup, hit the url <http://localhost:8000/api-docs/> to consume the api's.
Click the authorize button in Swagger and add value ```Token <token>``` or navigate to the `Auth` tab in the postman and add the above generated token value using `OAuth 2.0` type.


The project is using [PEP 8](https://www.python.org/dev/peps/pep-0008/) code styling and has [black](https://black.readthedocs.io/en/stable/) set up for auto-formatting with [flake8](https://flake8.pycqa.org/en/latest/) in place.

**Notes:**
- Makefile includes many other useful commands to interact with the application.
- The tests command uses the --keepdb option. It preserves the test database between test runs. It skips the create and destroy actions which can greatly decrease the time to run tests.

#### Things that are not included in the task due to time constraints:
- Database credentials are directly added in the settings/docker file. It should be confidential from a security perspective.
- There are multiple ways to build API's e.g function based views, class based views, generic views, viewsets. I used Viewsets in the application.
- DRF allows you to authenticate your application in many ways e.g basic, token, session etc. I used Token Authentication for the ease.
- Order itself can't be updated. Only Order lines can be updated. By update means, you can only update the values of certain fields, you can't be added or deleted order line in the update call for now. It can be added later.
- Application models have limited fields. For example Menu only contains name and price. It can have additional fields too e.g pizza flavors, size, crust etc. Similarly Order and OrderLine can also have additional fields.
- Mysql database is used instead of Postgresql because of the simplicity of task.
- Testcases are only added for views file. Few scenerios are missing but I covered all the main ones. serializers and models testcases couldn't be added due to time limitation.
- Using DEBUG=TRUE for debugging purpose. It shows the whole traceback of the exception. For development purpose it's fine but on production, its value should be FALSE.
- Python logs are being displayed on the console instead of file for the sake of simplicity. Sentry tool can be integrated to log the errors.
- All the APIs can be fully tested using swagger. Only data format of POST and UPDATE APIs is bit malfunctioned. Don't use the autogenerated data format. Please refer postman APIs for the correct data format.
