<img src="/diva_cloud/diva_docker/media/diva_docker.png" data-canonical-src="/diva_cloud/diva_docker/media/diva_docker.png" width="217" height="155" />

# diva_docker V0.3

Make [diva_django](/diva_django) working on Docker

Exchange file throught Django REST API.

> Include postgres service (DB)

> Include celery service (Task queue)

> Include redis service (Broker and Backend of celery)

---

# Run (if already installed)

> `cd diva_docker/` 

> `sh run_diva_cloud_docker.sh start`   # Launch the service in background

> `sh run_diva_cloud_docker.sh attach`  # Launch the service and show logs

> `sh run_diva_cloud_docker.sh`         # To see all commands

---

# Install

Make sure Docker is installed on your system:

- [Install Page](https://docs.docker.com/engine/install/)
  - On [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
  - On [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
  - On [Debian](https://docs.docker.com/engine/install/debian/)
  

## Install Automatically

> `cd diva_docker/` 

> `bash run_diva_cloud_docker.sh install` 

### Launch Automatically

- Without log

> `bash run_diva_cloud_docker.sh run` 

- With logs:

`bash run_diva_cloud_docker.sh attach` 

---

## Install Manually

#### Copy the docker build files:

There is two way to install the docker image.
Make the link of docker-compose file in diva_django according to your choice:
 
- A) Pull image from [docker hub](https://hub.docker.com/repository/docker/valm/diva_cloud/general)

> `cd diva_django/`

> `ln ../diva_docker/docker-compose_nobuild.yml docker-compose.yml`

- B) Build docker image from Dockerfile recipe (use that if you have changed something on the build)

> `cd diva_django/`

> `ln ../diva_docker/docker-compose.yml .`

> `ln ../diva_docker/Dockerfile .`

/!\ Symbolic link did not work

#### Replace the settings file with the Docker suitable one:

> `mv diva_cloud/settings.py diva_cloud/settings_backup.py`

> `ln ../diva_docker/settings.py diva_cloud/settings.py` # (See the DATABASES section)

#### Create a simlink for Diva python scripts:

> `ln -s diva-python/src diva_python_scripts`

#### Create container image:

> `sudo docker-compose build`

#### Launch container:

> `sudo docker-compose up`


##### Migrate (Django's model):

> `sudo docker ps`  # to get the id of the container (diva_django_web)

> `sudo docker exec  <container_id> python manage.py migrate`

> In case of problem you can access the container bash with:

> `sudo docker exec -t -i <container_id> bash`

> And then:

> \# `python manage.py makemigrations`

> \# `python manage.py migrate`

##### Create Jobtypes init, train and infer:

> `sudo docker exec <container_id> python -c "import os;os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diva_cloud.settings');from django.core.wsgi import get_wsgi_application;application = get_wsgi_application();from jobapp.models import JobType;jt = JobType(name='train');jt.save();jt = JobType(name='infer');jt.save();jt = JobType(name='init');jt.save()"`


##### Create admin user (name:admin; password:admin):

> `sudo docker exec <container_id> python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin','', 'admin')"`


##### Server run on: `http://127.0.0.1:8000/`

##### Login on: `http://127.0.0.1:8000/api-authlogin/` to see all the possible requests in `http://127.0.0.1:8000/`

##### Login on admin: `http://127.0.0.1:8000/adminlogin/?next=/admin`

##### Create Token to access API POST/DELETE/PUT `http://127.0.0.1:8000/adminauthtoken/token/add/`

---

## Configure

##### Server adress:

Change it on `diva_cloud/settings.py`

---

## Doc

- Docker Compose and Django

[https://docs.docker.com/compose/django/](https://docs.docker.com/compose/django/)

---

## API interactions use cases:

![DIVA REST SCHEM](/diva_cloud/diva_docker/media/DjangoDIVA-UseCase.png)

