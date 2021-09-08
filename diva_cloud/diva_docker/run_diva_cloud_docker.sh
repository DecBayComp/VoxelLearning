#!/usr/bin/env bash

cmd1="start"
cmd1expl="    #start containers in background"
cmd2="stop"
cmd2expl="     #stop containers"
cmd3="install"
cmd3expl="  #install and parameter diva-cloud on docker"
cmd4="attach"
cmd4expl="   #start with logs attached"
cmd5="rebuild"
cmd5expl="  #rebuild docker compose"
cmd6="test"
cmd6expl="     #Django test"

if [[ $1 == $cmd1 ]]; then
	docker-compose -f ../diva_django/docker-compose.yml up -d
elif [[ $1 == $cmd4 ]]; then
	docker-compose -f ../diva_django/docker-compose.yml up
elif [[ $1 == $cmd5 ]]; then
	docker-compose -f ../diva_django/docker-compose.yml build
elif [[ $1 == $cmd2 ]]; then
	docker-compose -f ../diva_django/docker-compose.yml stop
elif [[ $1 == $cmd3 ]]; then
	echo --START Install--
	echo "--1"
	echo "--Link Dockerfile in diva_django repo"
	ln  Dockerfile ../diva_django/.
	echo "--Done (The 'File exists' error is ok)"
	echo "-------"
	echo "--2"
	echo "--Link docker-compose.yml in diva_django repo"
	ln  docker-compose_nobuild.yml ../diva_django/docker-compose.yml
	echo "--Done (The 'File exists' error is ok)"
	echo "-------"
	echo "--3"
	echo "--backup diva_django settings"
	mv ../diva_django/diva_cloud/settings.py ../diva_django/diva_cloud/settings_backup.py
	echo "--Done (The 'same file' error is ok)"
	echo "-------"
	echo "--4"
	echo "--Link specific docker settings in diva_django repo"
	ln settings.py ../diva_django/diva_cloud/settings.py 
	echo "--Done (The 'File exists' error is ok)"
	echo "-------"
	echo "--5"
	echo "--Make a symbolic link of diva-python/src"
	rm -r ../diva_django/diva_python_scripts
	ln -s ../diva_django/diva-python/src ../diva_django/diva_python_scripts
	echo "--Done (The 'File exists' error is ok)"
	echo "-------"
	echo "--6"
	echo "--Build containers"
	docker-compose -f ../diva_django/docker-compose.yml build
	echo "--Done"
	echo "-------"
	echo "--7"
	echo "--Launch containers"
	docker-compose -f ../diva_django/docker-compose.yml up -d
	echo "--Done"
	echo "-------"
	echo "--8"
	echo "--Searching web container id"
	container_id=$(docker ps --filter "name=django_web" --format "{{.ID}}")
	echo "$container_id"
	echo "--Done"
	echo "-------"
	if [[ ! "$container_id"  ]]; then
	   echo "--No web container found"
	else
		echo "--9"
		echo "--Django migrate"
		docker exec  $container_id python manage.py migrate
		echo "--Done"
		echo "-------"
		echo "--10"
		echo "--Django makemigrations"
		docker exec  $container_id python manage.py makemigrations
		echo "--Done"
		echo "-------"
		echo "--11"
		echo "--Django migrate (2nd)"
		docker exec  $container_id python manage.py migrate
		echo "--Done"
		echo "-------"
		echo "--Creating jobtypes"
		docker exec $container_id python -c "import os;os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diva_cloud.settings');from django.core.wsgi import get_wsgi_application;application = get_wsgi_application();from jobapp.models import JobType;jt = JobType(name='train');jt.save();jt = JobType(name='infer');jt.save();jt = JobType(name='init');jt.save()"
		echo "--done"
		echo "-------"
		echo "--13"
		echo "--Creating Superuser"
		docker exec $container_id python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin','', 'admin')"
		echo "--Done (The 'already exist' error is ok)"
		echo "-------"
	fi
	echo "-------"
	echo "--Stop containers"
	docker-compose -f ../diva_django/docker-compose.yml stop
	echo "-------"
	echo "--END install--"
elif [[ $1 == $cmd6 ]]; then
	echo "-------"
	echo "--Searching web container id"
	container_id=$(docker ps --filter "name=django_web" --format "{{.ID}}")
	if [[ ! "$container_id"  ]]; then
		echo "--No web container found"
		echo "--Launch containers"
		docker-compose -f ../diva_django/docker-compose.yml up -d
		echo "--Done"
	fi
	echo "$container_id"
	container_id=$(docker ps --filter "name=django_web" --format "{{.ID}}")
	docker exec  $container_id python manage.py test -v 2 $2
	echo "-------"

else
	echo "-------------------"
	echo "Commands available:"
	echo "sh ${0##*/} $cmd1 $cmd1expl"
	echo "sh ${0##*/} $cmd2 $cmd2expl"
	echo "sh ${0##*/} $cmd3 $cmd3expl"
	echo "sh ${0##*/} $cmd4 $cmd4expl"
	echo "sh ${0##*/} $cmd5 $cmd5expl"
	echo "sh ${0##*/} $cmd6 $cmd6expl"
	echo "-------------------"
fi
