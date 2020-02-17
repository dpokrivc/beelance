# Simple python web application

Python webpy application running on uswgi server with nginx using docker connected to another docker-runned mysql database.

Web Server image base: https://github.com/tiangolo/uwsgi-nginx-docker

webpy framework: http://webpy.org/


## Installation:

1. Install docker: https://www.docker.com/
2. Install docker-compose: https://docs.docker.com/compose/install/
3. Launch docker
4. Clone this repository:
> git clone \<repositoryURL\>

IMPORTANT Windows users must use:
> git clone \<repositoryURL\> --config core.autocrlf=input
5. Run the application:
> docker-compose up

6. The application should become available on URL:
http://0.0.0.0:80\<groupid\> <br>
Or if you are running docker-toolbox :
http://192.168.99.100:80\<groupid\>

### Build / Rebuild

Upon changes in the code the docker image must be built again for the changes to take effect. Some changes might not get reflected even on build, which is when the --force-recreate attribute can be used.

$ docker-compose up --build 

### Prune / Recreate
If you need a completely fresh rebuild (WARNING this will remove all your docker images). This will reset the images including the database which is not necessary affected by only rebuilding the images

$ docker system prune -a

$ docker-compose up

### Config

The ip and ports for the web server and database is set with the .env file using the groupid variable.

## Deploy locally

Running the application outside of containers might be useful for development because the images does not need to be rebuilt for every change in the code. This is optional.

### Prerequisites:

mysql server

python =< 3.6.8

python packages: src/app/requirements.txt

### Run Datatbase:

Launch mysql at default port (3306)

$ systemctl start mysqld

Log in to database

$ sudo mysql -u root

Insert mysql queries:

CREATE database db;

USE db;

SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root');

GRANT ALL PRIVILEGES ON db.* TO 'root'@'localhost';

Then populate databse by posting mysql/sql/init.sql into mysql

### Run app

Edit src/app/models/database.py to point at local database server

$ cd src/app/

$ python3 src/app/main.py

