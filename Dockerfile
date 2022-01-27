FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
