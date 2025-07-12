# the order of the cmds are import for Docker's cacheing logic
FROM python:3.13.3

# Locations after this are relative to workdir
WORKDIR /usr/src/FastAPI_app

# install all dependencies of project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy the src code from project root (".") to dockerImage workdir root (".")
COPY . .

# cmd: uvicorn app.main:app --host 0.0.0.0 --port 8080
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]
