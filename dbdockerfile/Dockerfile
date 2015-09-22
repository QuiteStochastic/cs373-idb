FROM postgres
ADD ./.. /code
WORKDIR /code
USER postgres
RUN psql -c "ALTER USER postgres PASSWORD 'gotswe';"
RUN createdb housedowning -h 127.0.0.1
RUN apt-get install python3
RUN python3 app.py --make-tables
RUN psql -d housedowning -a -f ./raw_data/copy.sql
