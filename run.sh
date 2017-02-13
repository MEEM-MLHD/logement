docker-machine start logement
eval "$(docker-machine env logement)"
docker-compose run -e DJANGO_SETTINGS_MODULE=logement.settings -w /src web bash
