FROM python:3.10
WORKDIR site/

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--debugger"]