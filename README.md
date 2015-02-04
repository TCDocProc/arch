# arch
A user-friendly interface for presenting care pathways for a single patient using the PML language.

##Development Stack
**Backend**

- Django
- SQLite

**Frontend**

- Coffeescript
- Backbone.js
- Sass

**Continuous Integration**

- Jenkins

##Deployment

###OS X
*Prerequisite:* [Boot2Docker](https://github.com/boot2docker/boot2docker), [brew](http://brew.sh)

- `brew docker install`
- `boot2docker init`
- `boot2docker up`
- `docker build -t webapp .`
- `docker run -d -p 8000:80 webapp`

To run the web app first run `boot2docker ip` and then use http://IP_ADDRESS:8000

###Ubuntu

```
## Update apt-get
sudo apt-get update

## Install git
sudo apt-get install -y git

## Clone repo
git clone http://github.com/TCDocProc/arch

cd arch

## Install the webapp
sudo ./install

## Run the webapp
sudo ./run <port>

```

###Windows
Coming soon??
