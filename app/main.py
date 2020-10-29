from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import httpx
from starlette.config import Config
from okta_jwt.jwt import validate_token as validate_locally


config = Config(".env")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def retrieve_token(authorization):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'items',
    }
    url = config('OKTA_ISSUER') + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)


def validate_remotely(token):
    headers = {
        'accept': 'application/json',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': config('OKTA_CLIENT_ID'),
        'client_secret': config('OKTA_CLIENT_SECRET'),
        'token': token
    }
    url = config('OKTA_ISSUER') + '/v1/introspect'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return True
    else:
        raise HTTPException(status_code=400, detail=response.text)


def validate(token):
    # return validate_remotely(token)
    return validate_locally(
      token,
      config('OKTA_ISSUER'),
      config('OKTA_AUDIENCE'),
      config('OKTA_CLIENT_ID')
    )


# Open, Hello World route
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Get auth token
@app.post("/token")
def login(request: Request):
    return retrieve_token(request.headers['authorization'])


# Protected, get items route
@app.get("/items")
def read_items(token: str = Depends(oauth2_scheme)):
    if validate(token):
        return [
            {"id": 1, "name": "red ball"},
            {"id": 2, "name": "blue square"},
            {"id": 3, "name": "purple ellipse"},
        ]
