FROM python:3.9

WORKDIR /code

# Install pip requirements
COPY ./requirements.txt /code/requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]