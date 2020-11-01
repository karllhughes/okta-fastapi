FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copy the files into the Docker image
COPY requirements.txt /app/requirements.txt
COPY ./.env /app/.env
COPY ./main.py /app/main.py

# Install dependencies
RUN pip install -r requirements.txt
