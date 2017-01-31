#sh /src/scripts/wait.sh

cd /src
# collectstatic needs DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=logement.settings
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py makemessages -a
python manage.py compilemessages
uwsgi --socket :8000 --wsgi-file /src/logement/wsgi.py --chdir /src/logement --master --processes 4 --threads 2 --py-autoreload 3
