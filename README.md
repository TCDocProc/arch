A user-friendly interface for presenting care pathways for a single patient using the PML language.

## Development Stack
### Backend

| https://www.djangoproject.com | https://www.sqlite.org |
|------------|------------------|
| ![django-logo] | ![sqlite-logo] 

[django-logo]:http://www.fullstackpython.com/theme/img/django-logo-positive.png
[sqlite-logo]:https://iworkautomation.com/numbers/gfx/sqlite-logo.png

### Frontend

| http://coffeescript.org | http://backbonejs.org | http://sass-lang.com |
|---|---|---|
| ![coffeescript-logo] | ![backbone-logo] | ![sass-logo]

[coffeescript-logo]:http://coffeescript.org/documentation/images/logo.png
[backbone-logo]:http://backbonejs.org/docs/images/backbone.png
[sass-logo]:http://sass-lang.com/assets/img/logos/logo-b6e1ef6e.svg

### Continuous Integration

| http://jenkins-ci.org |
|---|
| ![jenkins-logo]

[jenkins-logo]:https://wiki.jenkins-ci.org/download/attachments/2916393/logo-title.png?version=1&modificationDate=1302753947000
##Deployment

###OS X

```
## Clone repo
git clone http://github.com/TCDocProc/arch

cd arch

## Install the webapp
./install_osx

## Run the webapp
./run <port>

```

To run the web app first run `boot2docker ip` and then use `http://IP_ADDRESS:PORT`

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
sudo ./install_ubuntu

## Run the webapp
sudo ./run <port>

```

### Windows
Coming soon??
