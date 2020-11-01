# FastAPI + Okta Authentication
This repository contains a REST API built on [FastAPI](https://fastapi.tiangolo.com/) and using [Okta](https://www.okta.com/) for OAuth authentication.

## Getting Started
_Using Docker_

- Build the Dockerfile: `docker build -t fastapi .`
- Run it locally: `docker run --rm -it --name fastapi -v $(pwd)/main.py:/app/main.py -p 8000:80 fastapi /start-reload.sh`
- View the app at [http://localhost:8000/items/5?q=somequery](http://localhost:8000/items/5?q=somequery).

