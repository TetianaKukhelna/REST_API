# Yalantis test project
### If you don't have docker do next few commands to install it
```
sudo apt install docker
``` 

To install docker use instruction for your operating system
https://docs.docker.com/engine/install/ubuntu/

If you want to run docker as non-root user then you need to add it to the docker group.
1. Create the docker group if it does not exist
```shell
$ sudo groupadd docker
```
2. Add your user to the docker group.
```shell
$ sudo usermod -aG docker $USER
```
3. Run the following command or Logout and login again and run (that doesn't work you may need to reboot your machine first)
```shell
$ newgrp docker
```

4. Check if docker can be run without root
```shell
$ docker run hello-world
```
5. Reboot if still got error
```shell
$ reboot
```

###Warning

The docker group grants privileges equivalent to the root user. 
For details on how this impacts security in your system, see
https://docs.docker.com/engine/security/#docker-daemon-attack-surface

Taken from the docker official documentation: https://docs.docker.com/engine/install/linux-postinstall/


### Now you can run project by command
```
make up
```
Docker pull image and run it in few minutes
Website will listen `0.0.0.0:3889` and you can do request

Final step.
Run command `make migrate`

Have fun!
