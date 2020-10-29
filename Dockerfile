FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# copy the dependencies and .env file
COPY requirements.txt /app/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# Copy code
COPY ./app /app
