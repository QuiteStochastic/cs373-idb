FROM python:3.4
RUN apt-get update
ADD . /code
WORKDIR /code
RUN apt-get install libpq-dev
RUN pip3 install -r requirements.txt

RUN apt-get -y install sudo
RUN apt-get -y install postgresql
RUN update-rc.d postgresql defaults
RUN service postgresql start && \
	sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'gotswe';" && \ 
	sudo -u postgres PGPASSWORD=gotswe createdb housedowning -h 127.0.0.1 && \	
	sudo python3 app.py --make-tables && \
	sudo -u postgres PGPASSWORD=gotswe psql -d housedowning -a -f ./raw_data/copy.sql
EXPOSE 80
CMD service postgresql start && \
	python3 app.py
