# Django Posts API

## ➡️ A Django API to store and retrieve posts made by users

## 🌐 Deploy live on [Django Posts](https://djangoposts.onrender.com/swagger/)

## 💻 Technologies used:
  - Python 3.12.0
  - Django 5.0.2
  - Django REST Framework 3.14.0
  - PostgreSQL 15.1.1.19
  - psycopg2 2.9.9
  - gunicorn 21.2.0
  - Pytest Django 4.8.0

## ⚙️ API Local Setup
  - Clone this repository to your local machine
  - Create a virtual environment with `python -m venv venv` and activate it
  - Install the required packages with `pip install -r requirements.txt`
  - Change the database settings in `config/settings/databases.py` by uncommenting the default database
  - Run the server with `python manage.py runserver`

## ❕Post Data Structure
  ```
    {
        "id": "number",
        "username: "string",
        "created_datetime: "datetime",
        "title: "string",
        "content: "string"
    }
  ```
  - #### A hidden field `updated_datetime` stores the datetime of the last update and it is available in the admin panel


## 💻 API Features and Endpoints
  #### Base URL: `djangoposts.onrender.com/`
  These are the available endpoints for the API:
  - `GET` ➔ `/posts/` ─ Retrieve all posts in the database. It has a default pagination of 10 items per page with links to previous and next pages.
    - Sample Success Response: `200 OK`
      ```
        {
          "count": 1,
          "next": null,
          "previous": null,
          "results": [{
            "id": 1,
            "username: "Username",
            "created_datetime: "2024-03-03T19:16:48.620489-03:00",
            "title: "New Title",
            "content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            }
          ]
        }
      ```
  - `GET` ➔ `/posts/{pk}/` ─ Retrieve data from a specific post.
      - Sample Success Response: `200 OK`
        ```
         {
            "id": 1,
            "username: "Username",
            "created_datetime: "2024-03-03T19:16:48.620489-03:00",
            "title: "New Title",
            "content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
          }
        ```
  - `POST` ➔ `/posts/` ─ Create a new entry for a post in the database. All fields are required.
    - Request Body: `username`: string, `title`: string, `content`: string
    - Sample Success Response: `201 Created`
      ```
       {
          "id": 1,
          "username: "Username",
          "created_datetime: "2024-03-03T19:16:48.620489-03:00",
          "title: "New Title",
          "content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
      ```
  - `PATCH` ➔ `/posts/{pk}/` ─ Update a post in the database. If the request body is empty, it will return a `400 Bad Request`.
    - Request Body: `title`: string, `content`: string
    - Sample Success Response: `200 OK`
      ```
       {
          "id": 1,
          "username: "Username",
          "created_datetime: "2024-03-03T19:16:48.620489-03:00",
          "title: "Modified Title",
          "content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
      ```
         - Updates will only be performed on the `title` and `content` fields, other fields in the request will be ignored.

  - `DEL` ➔ `/posts/{pk}/` ─ Delete a post from the database.
    - Success Response: `204 No Content`

  #### These endpoints can also be checked and tested on the `/swagger/` endpoint.


  ## 🔧 Tests
   #### This project has a 100% coverage rate using `pytest-django`, and all tests can be found in the `postlist/tests/` directory.



    
