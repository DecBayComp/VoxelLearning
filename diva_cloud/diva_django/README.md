# diva_django V0.8

Exchange file throught Django REST API.

## Install

#### Clone

> $ `git clone --recurse-submodules git@gitlab.pasteur.fr:diva/diva-cloud.git`

> $ `cd diva_django/`  

#### Install Python3 dependencies:

> $ `apt-get update`

> $ `apt-get install python3-pip python3-dev`

#### Create env (Python3):

> $ `python -m venv .env`

> $ `source .env/bin/activate`

#### Install Python packages:

> $ `pip install -r requirements.txt`

#### Install Python packages for Diva python scripts:

> $ `pip install -r diva-python/requirements.txt`

#### Create a simlink for Diva python scripts:

> $ `ln -s diva-python/src diva_python_scripts`

#### Install Postgres database:

> $ `apt-get update`

> $ `apt-get install libpq-dev postgresql postgresql-contrib`

> $ `sudo -u postgres psql`

> postgres=# `CREATE DATABASE diva;`

> postgres=# `CREATE USER django WITH PASSWORD 'pass';`

> postgres=# `ALTER ROLE django SET client_encoding To 'utf8';`

> postgres=# `ALTER ROLE django SET default_transaction_isolation TO 'read committed';`

> postgres=# `ALTER ROLE django SET timezone TO 'UTC';`

> postgres=# `GRANT ALL PRIVILEGES ON DATABASE diva TO django;`

> postgres=# `\q`

##### If you want to run unit tests:

> postgres=# `ALTER USER django CREATEDB;`

#### Install Celery (A task queue to make diva-cloud asynchronous):

> Nothing to install its on the requirements.txt 

#### Install redis (Broker and Backend of Celery)
 
> Nothing to install its on the requirements.txt 

#### Launch Celery:

> `celery -A celery_tasks worker --loglevel=info`

#### Migrate (Django's model):

> $ `python manage.py migrate`

#### Start the development server:

> $ `python manage.py runserver`

##### Server run on: `http://127.0.0.1:8000/`

##### Create a supeuser account

> $ `python manage.py createsuperuser --username=<adminlogin>`

##### Login on: `http://127.0.0.1:8000/api-authlogin/` to see all the possible requests in `http://127.0.0.1:8000/`

##### Login on admin: `http://127.0.0.1:8000/adminlogin/?next=/admin`

##### Create Token to access API POST/DELETE/PUT `http://127.0.0.1:8000/adminauthtoken/token/add/`

##### Access shell

> $ `python manage.py shell`

---

## Doc

-Install Django, Django REST Framework & Configure a file upload

[https://www.techiediaries.com/django-rest-image-file-upload-tutorial/](https://www.techiediaries.com/django-rest-image-file-upload-tutorial/)

---

## API Use Case:

![DIVA USE CASE](/diva_django/media/DjangoDIVA-UseCase.png)

---

##  DIVA interactions with "DIVACloud":

![DIVA CLOUD ACTION](/diva_django/media/DjangoDIVA-Interactions.png)

---

## API database model:

![DIVA DATABASE MODEL](/diva_django/media/DjangoDIVA-DBschem.png)

## Django repository:

![DIVA DJANGO REPO](/diva_django/media/DjangoDIVA-DJANGO.png)

