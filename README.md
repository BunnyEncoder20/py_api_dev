# Python API Development

- Will be using this repo for learning API development using Python.

## Tech Stack

- **Fast API**: Cause it's build keeping api development in mind and also has a auto documentation feature (becasue it is important to document how an api works)
- **Postgres**: SQL database (almost all the same)
- **SQL Alchemy**: ORM, most standard one for python frameworks, most popular

---

## Documentations

- Please visit the [FastAPI Documentations](https://fastapi.tiangolo.com/tutorial/first-steps/#what-is-openapi-for) Page.
- It literally has everything, from setting up venvs to everything to write robost APIs in pyhton

---

## Backend API Dev

- Backend api dev, is just making a bunch of path operations
  ![alt text](image.png)

---

## Things Learned

1. Central Env variable loading

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

2. Voting / Likes systems
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




---

### Important Commands

1. Starting the API server

```text
uvicorn app.main:app --reload
```
