docker-machine start logement
eval "$(docker-machine env logement)"
export URL='http://'$(docker-machine ip logement)
python -mwebbrowser $URL
docker-compose up
