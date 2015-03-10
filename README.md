[![Build Status](http://jenkins.kev.sh/job/DjangoMasterUnitTests/badge/icon)](http://jenkins.kev.sh/job/DjangoMasterUnitTests/) 

A user-friendly interface for presenting care pathways for a single patient using the PML language.

## Development Stack
### Backend

| https://www.docker.com | https://www.djangoproject.com | https://www.sqlite.org |
|------|------------|------------------|
|![docker-logo] | ![django-logo] | ![sqlite-logo] 

[docker-logo]:http://core0.staticworld.net/images/idge/imported/article/nww/2013/12/docker-100275159-orig.jpg
[django-logo]:http://www.fullstackpython.com/theme/img/django-logo-positive.png
[sqlite-logo]:https://iworkautomation.com/numbers/gfx/sqlite-logo.png

### Frontend

| http://bower.io | http://coffeescript.org | http://backbonejs.org | http://sass-lang.com |
|---|---|---|---|
|![bower-logo]| ![coffeescript-logo] | ![backbone-logo] | ![sass-logo]

[bower-logo]:https://camo.githubusercontent.com/aad5f0385a2d8524cb366a1bad62bc74e797743a/687474703a2f2f692e696d6775722e636f6d2f516d47485067632e706e67
[coffeescript-logo]:https://raw.githubusercontent.com/ServiceStack/Assets/master/img/livedemos/techstacks/coffeescript-logo.png
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

###Ubuntu Install Without Docker

```
## Update apt-get
sudo apt-get update

## Install git
sudo apt-get install -y git

## Clone repo
git clone http://github.com/TCDocProc/arch

cd arch/

## Install the webapp and run it
./nodocker_install

```
## Feature Listing

###Authentication - Complete

Use /accounts/signup/ to register your own user.

A test user is provider at 
	Username	: test
	Pass	 	: testpass

###Pathway Listing

On Login you will see either an interface or an upload screen. If you are on the upload screen you can upload an example xml.

This will be converted to josn by the xml to json parser.

Then you will be re-directed to you Pathway view.

###Pathway View

Panning and Zooming is done by clicking through the interface. Metadate shows up when you zoom in fully.

###Responsiveness

The whole view is responsiveness.

### Windows
Coming never
