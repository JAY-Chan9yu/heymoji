FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
RUN pip install --upgrade pip
# docker image 빌드시 requirements 설치하려면 사용
#COPY . .
#RUN pip install -r requirements.txt
