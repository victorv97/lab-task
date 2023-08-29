# TODO List API
___________________________________

This is a simple RESTful API application for managing TODO list based on Django Rest Framework.

## Install and run
___________________________________

Download the source code via:

    git clone https://github.com/victorv97/lab-task.git

### Using Docker (compose)

    ...\lab-task> cd lab_task
    ...\lab-task\lab_task> docker-compose build

Run the app with

    ...\lab-task\lab_task> docker-compose up

The necessary migrations and all the tests will be run first. After that the server will start.

### Manually
Create virtual environment

    ...\lab-task> cd lab_task
    ...\lab-task\lab_task> python -m venv env
    ...\lab-task\lab_task> env/Scripts/activate.bat

Install requirements
    
    (env)...\lab-task\lab_task> pip install -r requirements.txt

Run the app with

    (env)...\lab-task\lab_task> python manage.py runserver

Run the tests

    (env)...\lab-task\lab_task> python manage.py test

# REST API Reference
___________________________________