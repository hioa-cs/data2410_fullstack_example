# A full stack example for data2410

## Running each container with docker
This example uses the `skynet` network, created with `$ docker network create skynet`. If you want to use your own network, replace `skynet` with the name of your own network.


Standing in the source repo, start the database like this:
```
$ docker run -it --rm -d --name mysql1 --network skynet -e MYSQL_ROOT_PASSWORD=my-secret-pw -v $(pwd)/sql:/docker-entrypoint-initdb.d mysql
```
Notice the `-d` - this will make the container run in the background. If you have docker for mac or docker for windows installed, you should be able to see a container named `mysql1` running.

The backend, which hosts both the API and the frontend can now be started like this:
```
$ docker run -it --rm --name pyback --network skynet -p 5000:5000 -v $(pwd)/python_backend/server.py:/var/fullstack/server.py -v $(pwd)/frontend/:/var/fullstack/frontend/ -t python_backend python /var/fullstack/server.py
```

## Running with docker compose
TODO