FROM python:3.10.12
COPY requirements-dev.txt /project/
COPY requirements.txt /project/
RUN pip install --no-cache-dir --upgrade -r /project/requirements-dev.txt -r /project/requirements.txt
COPY . /project
WORKDIR /project
CMD alembic upgrade head && uvicorn src.__init__:app --host 0.0.0.0 --port 8000 --reload