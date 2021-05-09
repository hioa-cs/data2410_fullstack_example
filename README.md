# A full stack example for data2410

## Running each container with docker
This example uses the `skynet` network, created with `$ docker network create skynet`. If you want to use your own network, replace `skynet` with the name of your own network.

### Starting the database
The database uses the official MySQL docker image directly, with the contents of the `sql` directory mounted inside (e.g. the `sql` directory will be shared with the container)
Standing in the source repo, start the database like this:
```
$ docker run -it --rm -d --name mysql1 --network skynet -e MYSQL_ROOT_PASSWORD=my-secret-pw -v $(pwd)/sql:/docker-entrypoint-initdb.d mysql
```
Notice the `-d` - this will make the container run in the background. If you have docker for mac or docker for windows installed you should be able to see a container named `mysql1` running.

### Build and run the backend
The backend, which hosts both the API and the frontend, has a couple of python dependencies which is nice to build into the container. Build with:
```
 $ docker build -t python_backend  ./python_backend/
```
This will result in an image named `python_backend`. You should be able to see that with `$ docker images` or by clikcing the "Images" label in docker for desktop.
The backend can now be started like this:
```
$ docker run -it --rm --name pyback --network skynet -p 5000:5000 -v $(pwd)/python_backend/server.py:/var/fullstack/server.py -v $(pwd)/frontend/:/var/fullstack/frontend/ -t python_backend python /var/fullstack/server.py
```

## Integrating with Google sign-in
The app has Google sign-in integration for authentication and will allow you to log in using your Google user ID.

>**NOTE** The Google client-ID used in the lecture has been removed so you need to generate and add your own for sign-in to work. If you don't you'll get an authorization error when trying to sign in.

### Follow these steps to get Google sign-in to work:
- Create your App and credentials following this guide: https://developers.google.com/identity/sign-in/web/sign-in. You may need to create a project before you can do so and you need to be registered for a Google developer profile.
- Once you have your credentials, add them to the source code:
  - Update the HTML here: https://github.com/hioa-cs/data2410_fullstack_example/blob/9fc8f07630ffad2644a76db3f45dbd1c15e03ba6/frontend/index.html#L9
  - Update the backend here: https://github.com/hioa-cs/data2410_fullstack_example/blob/9fc8f07630ffad2644a76db3f45dbd1c15e03ba6/python_backend/server.py#L16
- Add your own Gihtub account(s) to the MySQL table here, replacing Alfred / Derek: https://github.com/hioa-cs/data2410_fullstack_example/blob/master/sql/my_database.sql#L23
- Play around with different access levels - levels 10 and 100 should load different "secrets". 

## Running with docker compose
TODO
