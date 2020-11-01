# FastAPI + Okta Authentication
This repository contains a REST API built on [FastAPI](https://fastapi.tiangolo.com/) 
and using [Okta](https://www.okta.com/) as an authorization server.

## Getting Started
_Using Docker_

- Build the Dockerfile: `docker build -t fastapi .`
- Run it locally: `docker run --rm -it --name fastapi -v $(pwd)/main.py:/app/main.py -p 8000:80 fastapi /start-reload.sh`
- View the app at [http://localhost:8000/](http://localhost:8000/)

_Using Local Python/Virtual Env_

- Install dependencies: `pip install -r requirements.txt`
- Run the app with Uvicorn: `uvicorn main:app --reload`
- View the app at [http://localhost:8000/](http://localhost:8000/)
