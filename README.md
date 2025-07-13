# Python API Development

- Will be using this repo for learning API development using Python.

## Tech Stack

- **Fast API**: Cause it's build keeping api development in mind and also has a auto documentation feature (becasue it is important to document how an api works)
- **Oauth2**: JWT and OAuth for authentication of users
- **Postgres**: SQL database (almost all the same)
- **SQL Alchemy**: ORM, most standard one for python frameworks, most popular
- **Alembic**: Database Migration Tool used to make revisions (commits) for SQL Database Tables
- **Docker**:

---

## Documentations

- Please visit the [FastAPI Documentations](https://fastapi.tiangolo.com/tutorial/first-steps/#what-is-openapi-for) Page.
- It literally has everything, from setting up venvs to everything to write robost APIs in pyhton
- How to activate and deactivate _virtual env_ which making python projects:
```python
source .venv/bin/activate
```
```python
deactivate
```

---

## Backend API Dev

- Backend api dev, is just making a bunch of path operations
  ![alt text](image.png)

---

## Things Learned

1. **Central Env variable loading**

   - done using config file using pydantic-settings package:BaseSettings
   - Introduces:
     - Type safety
     - Env variable validation
     - Centralized config loading. Single source of truth
     - Gives Auto complete and IDE help (from pydantic-settings package)
   - Now instead of loading env variables in each file, we just import the settings/config class from the app.config and use the follow way to access env variables
    ```python
    from app.config import settings
    env_variable = settings.ENV_NAME
    ```

2. **Voting / Likes systems**
   1. DB Properties
      1. User should be able to like a post once only
      2. For this we would need 2 cols atleast [postID, userID] and each combination of these would need to be unique
      3. we can achieve that by using **composite keys** in PgSQL. **Composite Keys** are simpily a primary key, which spans multiple columns
      4. As primary keys can only be unique, this will take care of our requirement.
   2. Vote Route
      1. Path will be at "/vote"
      2. The user id will be extracted from the JWT token
      3. The body will contain the id of the post the user is voting on as well as the direction of the vote.
      4. A vote direction of 1 means we want to add a vote, a direction of O means we want to delete a vote.w
    3. Sending the Votes of Post along with Post data object
        1. We would want to send back the Post's votes back to along with the rest the post data.
        2. In order to do that, we would have to join two tables together.
        3. We can do that is PgSQL using JOIN:
        ```python
        SELECT title, content, email FROM posts_table_v2
        LEFT JOIN users ON posts_table_v2.user_id = users.id
        ```
        4. We can specify which cols of table by using the tablename.colname (tablename.* for all columns)

3. **Alembic - DB Migration Tool**
    1. SqlAlchemy Limitations
        - When it comes to upgrading our tables, SqlAlchemy cannot change already made tables and cols
        - This is becasue if the table already exists, it'll not add any new changes to the tables casue it is already there. Hence we cannot change or add new cols
        - Till now I was dropping the old tables and restarting the server to make changes / adding cols to a table
    2. Where Alembic comes into picture
        - Why DB migration tool ?
            - Developers can track changes to code and rollback code easily with GIT. Why can't we do the same for database models/tables
            - Database migrations allow us to incrementally track changes to database schema and rollback changes to any point in time
            - We will use a tool called **Alembic** to make changes to our database
            - **Alembic** can also automatically pull database models from Sqlalchemy and generate the proper tables
        - Intigration & Setting up
            1. Install Alembic
            2. Init Alembic dir: this will create the "alembic" dir and alembic.ini file. ensure these are outside the app dir (in the root of project)
            ```python
            (.venv) alembic init alembic
            ```
            3. Becasue we want Alembic to work with SqlAlchemy,
                1. we need to give it access to the Base object.
                2. Also it needs access to all ORM models, so we import the models module.
                3. For makingthe DB url, we need the settings class instance from the config file also.
            4. Also these are imported into the alembic/env.py file:
            ```python
            from app.database import Base
            from app import models
            from app.cofig import settings

            # overriding the sqlalchemy.url from alembic.ini file here
            config.set_main_option(
                "sqlalchemy.url", f"postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
            )
            ```
    3. Usage | ref: [Alembic Documentations](https://alembic.sqlalchemy.org/en/latest/api/ddl.html)
        1. Creating a new revision:
            - kinda like a making a change file (use a -m for msg)
            - commands entered in teminal)
            ```cmd
            alembic revision -m "create posts table"
            ```
            - Generates the versions folder (if not there) and create a new revision (change) under it
            - In the revision file , we have to MANUALLY add the logic for each change to the tables/cols. Example given:
            - there has to be a upgrade: for adding changes and a Downgrade func for removing the above changes
            ```python
            def upgrade() -> None:
                """Upgrade schema."""
                op.create_table('Posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                )


            def downgrade() -> None:
                """Downgrade schema."""
                op.drop_table('Posts')
            ```
        2. Checking Current revision of Database
            - cmd in terminanl:
            ```cmd
            alembic current
            ```

        3. Upgrade cmd
            - cmd to update (goto) a specified revision (via revision number present in revision file) of database.
            - kinda like a commit in git
            ```cmd
            alembic upgrade <revision ID>
            alembic upgrade +1
            alembic upgrade +2
            ```
            - If it's first table created through alembic, there will be an extra table called alembic_version which stores all the revisions (do not touch that)
            - New for every change we make to the Table, we can make it's respectve revision: Eg: adding a col to posts table:
            ```cmd
            alembic revision -m "adds content col to posts table"
            ```
            - after which we can edit it's revision file: (notice this one will have a down_revision field also)
            ```python
            def upgrade() -> None:
                """Upgrade schema."""
                op.add_column(
                    'Posts',
                    sa.Column('content', sa.String(), nullable=False)
                )


            def downgrade() -> None:
                """Downgrade schema."""
                op.drop_column('Posts', 'content')
            ```

        4. heads cmd: displays the lastest revision made (aka head)
        ```cmd
        alembic head            # displays the head
        alembic upgrade head    # upgrades (commits) the head revision (latest)
        ```

        5. downgrade cmd
            - used to rollback the changes made during a revision
            - after the keyword, enter the down_revision ID for revision (change)
            - or we can add a number (Eg: -1 will take one revision back, -2 will take 2 revisions back)
            ```cmd
            alembic downgrade <down_revision ID>
            alembic downgrade -1
            alembic downgrade -2
            alembic downgrade base          # all the way down to base
            ```

        6. Do check out the revision files of this project to see how to actually write the upgrade and downgrade logic, it is NOT the same as writing the Pydantic ORM models.

4. Fixing the CORS problem in FastAPI
    - We use the CORSMiddleware by:
        1. Importing it
        2. creating a list of allowed origins
        3. Add it as a "middleware" to your FastAPI app

5. Dockerizing our app
    1. We start by building a custom image. We can use the Official Python image as a base image in the file:
    ```cmd
    Dockerfile
    ```
    2. Run to build cmd to build the docker custom image file for our app (. at end location of Dockerfile):
    ```cmd
    docker build -tag fastapi_app_image .
    ```
    3.Instead of using Docker run, we will use Docker compose cause it makes it way easier (by putting all cmds and flags into a file) for spinning up our images and tearing them down. Make a file named:
    ```cmd
    docker-compose.yml
    ```
    4. After writing the code into the `docker-compose.yml` file, we can spin up the image by cmd (-d = detach, runs the containers in background):
    ```cmd
    docker-compose up -d
    ```
6. Docker Desktop App
    - Once the containers are running, we can access useful features like logs and executable terminal right from the Docker app.
    - Synced local project dir and comtainer project dir by adding a **binding volumne**

7. Start Scripts
    - There might be a lot of commands which are needed to be run before starting our FastAPI server. Eg: running all alembic migrations to make the required tables of our DB
    - Hence we include a start script which are run all of our project starting commands in one place
    - Instead of chaining everything to one command in the docker-compose file, It is much easier to read, comment and expand. Eg:
    ```start.sh
    #!/bin/bash

    # Wait until DB is ready (optional)
    echo "[Server] ⏳ Waiting for DB to be ready..."
    sleep 3

    # Run Alembic migrations
    echo "[Alembic] ⬆️ Running migrations..."
    alembic upgrade head

    # Start the server
    echo "[Uvicorn] 🚀 Starting FastAPI server..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    - Make it an executable:
    ```cmd
    chmod +x start.sh
    ```
    - Finally add the command into the api_service in docker-compose file to run this start script:
    ```docker-compose.yml
    command: ["./start.sh"]
    ```




---

## Important Commands

1. Starting the API server

```text
uvicorn app.main:app --reload
```

2. Activating venv (mac)
```cmd
source .venv/bin/activate
```

3. Making requirements.txt file (to help install project with exact packages and their versions)
```cmd
uv pip freeze > requirements.txt
```

4. To use the requirements file to install all the dependencies of the project:
```cmd
pip install -r requirements.txt
```

5. Building a docker image (ensure you have made the Dockerfile beforehand in root of project, finaly . represents where the Dockerfile is)
```cmd
docker build -t fastapi_app_image .
```

6. Scanning for docker images
```cmd
docker image ls
```
