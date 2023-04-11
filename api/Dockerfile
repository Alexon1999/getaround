FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /home/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /home/app/

CMD gunicorn app:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker