FROM python:3.4
ADD . /code
WORKDIR /code
RUN apt-get install libpq-dev
RUN pip3 install -r requirements.txt
CMD python3 app.py
