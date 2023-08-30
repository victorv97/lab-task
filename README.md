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

# Authorization and authentication
___________________________________
The service uses JWT authentication. To access the API do sign up first. Then log in with username and password to 
obtain the access and refresh tokens.

### Signup
Creates a new user with hashed password and returns user's data.

 **Request**

    POST /api/signup/

POST body:

    {
        "first_name": "name",
        "last_name": "last name",
        "username": "username",
        "password": "password"
    }

**Response**

    HTTP 201 Created
    Allow: OPTIONS, POST
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 1,
        "first_name": "name",
        "last_name": "last name",
        "username": "username",
        "password": "pbkdf2_sha256$600000$8xWZcNVr6UvA3bB8OILiLP$6cIyaPpzDJWJhnC6ilQRSMOKeyXVfMpC5FoeMSA5nzE="
    }


### Login
Takes a set of user credentials and returns an access and refresh JWT pair to prove the authentication of those credentials.

 **Request**

    POST /api/login/

POST body:

    {
        "username": "username",
        "password": "password"
    }

**Response**

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NTk5MDQ5OSwiaWF0IjoxNjkzMzk4NDk5LCJqdGkiOiJlY2JmNmZiNGY1MGQ0MmUwOTY4YmQ4OWViYmNiOTMzMiIsInVzZXJfaWQiOjl9.nqCAvDcF7STbzTuhOFGhf1HpmsFb4Zxw_uQrh2obnv0",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzNDg0ODk5LCJpYXQiOjE2OTMzOTg0OTksImp0aSI6IjVhMzRlMWU3ZTYxMjRhNTc5M2NhMzczYzFjZDBiNWQzIiwidXNlcl9pZCI6OX0.yWs3J1VtDbXdjBoHWd5ujb7s8nrIZdeIQYA_Y8AmsHc"
    }

### Token Refresh
Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid.

 **Request**

    POST /api/login/refresh

POST body:

    {
        "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NTk5MDQ5OSwiaWF0IjoxNjkzMzk4NDk5LCJqdGkiOiJlY2JmNmZiNGY1MGQ0MmUwOTY4YmQ4OWViYmNiOTMzMiIsInVzZXJfaWQiOjl9.nqCAvDcF7STbzTuhOFGhf1HpmsFb4Zxw_uQrh2obnv0"
    }

**Response**

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzNDg1MTI2LCJpYXQiOjE2OTMzOTg0OTksImp0aSI6IjQ2Y2FhYWM3NDc2NjQ4MDQ5Y2ZlMjFlMjgyMDQyZjg1IiwidXNlcl9pZCI6OX0.4eQXfzbNCQYhokFxz5DtjFNR0QQjFJB0eTg1X8kv7Lc"
    }


You can provide authentication credentials, for example, with **Authorization** header using the **Bearer** schema:

    Authorization: Bearer <access_token>


# REST API Reference
___________________________________

#### Try the API endpoints [here](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/victorv97/lab-task/main/openapi-schema.yml#/).

Don't forget to provide authentication credentials. The service is available for authorized users only.

### Get Task List
Returns a paginated list of all tasks in the app. Allows filtering by status field.

 **Request**

    GET /api/task-list/

 **Response**

    HTTP 200 OK
    Allow: OPTIONS, GET
    Content-Type: application/json
    Vary: Accept
    
    [
        {
            "id": 1,
            "title": "sample title",
            "description": "some description",
            "status": 0,
            "user_id": 1
        },
    ]

### Get User Task List
Returns a list of all the specified user's tasks. Allows filtering by status field.

 **Request**

    GET /api/user-task-list/{user_id}/

 **Response**

    HTTP 200 OK
    Allow: OPTIONS, GET
    Content-Type: application/json
    Vary: Accept
    
    [
        {
            "id": 2,
            "title": "sample title 2",
            "description": "some description",
            "status": 2,
            "user_id": 1
        },
    ]

### Get Task

Returns information about a specified task.

 **Request**

    GET /api/task/{task_id}/

 **Response**

    HTTP 200 OK
    Allow: OPTIONS, GET
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 5,
        "title": "sample title 5",
        "description": "another description",
        "status": 1,
        "user_id": 1
    }


### Create Task

Creates new task and returns information about this one.

 **Request**

    POST /api/create-task/

POST body:

    {
        "title": "some title",
        "description": "some description",
        "status": 0,
        "user_id": 1
    }

 **Response**

    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 10,
        "title": "some title",
        "description": "some description",
        "status": 0,
        "user_id": 1
    }


### Update Task

Updates an existing task by specified id and returns information about the updated task.
Allows partial updating.

The task can be updated by the owner only.

 **Request**

    POST /api/update-task/{task_id}/

POST body:

    {
        "title": "updated title",
        "description:: 'updated description",
    }

 **Response**

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 10,
        "title": "updated title",
        "description": "updated description",
        "status": 0,
        "user_id": 1
    }

### Mark Completed Task

Updates status field of an existing task to COMPLETED by specified id.
Returns information about the updated task.

The task can be updated by the owner only.

 **Request**

    POST /api/task/{task_id}/mark-completed/



POST body:

    { }

 **Response**

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 10,
        "title": "updated title",
        "description": "updated description",
        "status": 2,
        "user_id": 1
    }

### Delete Task

Deletes an existing task by specified id and returns the corresponding success message.

The task can be deleted by the owner only.

 **Request**

    DELETE /api/delete-task/{task_id}/

 **Response**

    HTTP 200 OK
    Allow: DELETE, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    "Task 10 successfully deleted"


### Filtering and pagination

Such API endpoints as **task-list** and **user-task-list** allow filtering by status.

For example:

 **Request**

    GET /api/task-list/?status=1

 **Response**

    HTTP 200 OK
    Allow: GET, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    [
        {
            "id": 5,
            "title": "sample title 5",
            "description": "another description 5",
            "status": 1,
            "user_id": 1
        },
        {
            "id": 8,
            "title": "sample title 8",
            "description": "another description 8",
            "status": 1,
            "user_id": 1
        }
    ]


The API endpoint **task-list** supports pagination. The page size is set to 5 by default

 **Request**

    GET /api/task-list/?page=2

 **Response**

    HTTP 200 OK
    Allow: GET, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    [
        {
            "id": 6,
            "title": "sample title 6",
            "description": "another description 6",
            "status": 0,
            "user_id": 1
        },
        {
            "id": 7,
            "title": "sample title 7",
            "description": "another description 7",
            "status": 0,
            "user_id": 2
        },
        {
            "id": 8,
            "title": "sample title 8",
            "description": "another description 8",
            "status": 1,
            "user_id": 1
        },
        {
            "id": 9,
            "title": "some title 9",
            "description": "some description 9",
            "status": 0,
            "user_id": 5
        },
        {
            "id": 10,
            "title": "some title 10",
            "description": "some description 10",
            "status": 0,
            "user_id": 1
        }
    ]

