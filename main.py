from typing import List
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import httpx
from starlette.config import Config
from okta_jwt.jwt import validate_token as validate_locally


config = Config('.env')

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class Item(BaseModel):
    id: int
    name: str


def retrieve_token(authorization, issuer):
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
    url = issuer + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)


def validate_remotely(token, issuer, clientId, clientSecret):
    headers = {
        'accept': 'application/json',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': clientId,
        'client_secret': clientSecret,
        'token': token,
    }
    url = issuer + '/v1/introspect'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return True
    else:
        raise HTTPException(status_code=400, detail=response.text)


def validate(token: str = Depends(oauth2_scheme)):
    # Remote validation
    return validate_remotely(
        token,
        config('OKTA_ISSUER'),
        config('OKTA_CLIENT_ID'),
        config('OKTA_CLIENT_SECRET')
    )
    # Local validation
    return validate_locally(
        token,
        config('OKTA_ISSUER'),
        config('OKTA_AUDIENCE'),
        config('OKTA_CLIENT_ID')
    )


# Open, Hello World route
@app.get('/')
def read_root():
    return {'Hello': 'World'}


# Get auth token
@app.post('/token')
def login(request: Request):
    return retrieve_token(request.headers['authorization'], config('OKTA_ISSUER'))


# Protected, get items route
@app.get('/items', response_model=List[Item])
def read_items(valid: bool = Depends(validate)):
    return [
        {'id': 1, 'name': 'red ball'},
        {'id': 2, 'name': 'blue square'},
        {'id': 3, 'name': 'purple ellipse'},
    ]
