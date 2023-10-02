pip freeze > requirements.txt
docker-composer up -d --build
./manage.py startapp taskapp
docker exec -it django /bin/sh