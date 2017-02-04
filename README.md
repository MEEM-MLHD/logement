# logement

## Install

On linux, run the following command

```
git clone https://github.com/MEEM-MLHD/logement
cd logement
docker-compose up
```

Due to sync issues between containers, you may also need to migrate and create a superuser. See src/scripts/start_web.sh for more information.


If you want to recover data, fill the db with the appropriate dump

```
eval "$(docker-machine env logement)"  # not for Linux
docker-compose run db /srv/data/backup/restore_db.sh
```

## Help on docker on OSX

Create a docker machine

```
docker-machine create --driver virtualbox --virtualbox-memory 8096 logement
```

List all docker machines

```
docker-machine ls
```

Stop a docker machine

```
docker-machine stop logement
```

Start a docker machine

```
docker-machine start logement
```
Set env variable the right way

```
eval "$(docker-machine env logement)"
```

To get the VM IP address

```
docker-machine ip logement
```

docker-compose

```
docker-compose build logement
docker-compose build --no-cache logement
docker-compose run logement command
docker-compose up logement
docker-compose stop
```

Install docker-compose

```
sudo -i
mkdir -p /opt/bin
curl -L https://github.com/docker/compose/releases/download/1.8.1/docker-compose-`uname -s`-`uname -m` > /opt/bin/docker-compose
chmod +x /opt/bin/docker-compose
exit
```
