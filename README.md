# Python API Development

- Will be using this repo for learning API development using Python.

### Tech Stack

- **Fast API**: Cause it's build keeping api development in mind and also has a auto documentation feature (becasue it is important to document how an api works)
- **Postgres**: SQL database (almost all the same)
- **SQL Alchemy**: ORM, most standard one for python frameworks, most popular

---

### Setting up venv in Py:

1. command to make a venv named `venv`:

```
python3 -m venv <name>
```

or use uv (ultra fast py pkg manager)

```
uv venv
```

- "venv" is a general practice name for all venvs
- should create a folder with the name "venv"

2. Activate the venv:

```
source venv/bin/activate
```

- we should something like this in your terminal prompt:

```
> (venv)
```

3. Install our dependencies

```
pip install fastapi uvicorn
```

- `uvicorn` is the ASGI server commonly used to run FastAPI apps.

4. (Optional) Freeze Dependencies

- This creates a requirements.txt file which can be used to recreate the venv for another machine or cloud

```
pip freeze > requirements.txt
```

---
