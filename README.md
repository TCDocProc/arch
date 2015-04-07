<!--[![Build Status](http://jenkins.kev.sh/job/DjangoMasterUnitTests/badge/icon)](http://jenkins.kev.sh/job/DjangoMasterUnitTests/)--> 

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
./install_osx [options...]

OPTIONS:
   -h      Show usage info
   -s      Skip brew installation

## Run the webapp
./watch_run_osx <port>

```

The last command returns `Running on: http://<boot2docker-ip>:<port>` you can open the webapp at the returned URL.

###Ubuntu (Without Docker)

```
## Update apt-get
sudo apt-get update

## Install git
sudo apt-get install -y git

## Clone repo
git clone http://github.com/TCDocProc/arch

cd arch/

## Install the webapp
./arch_ubuntu install

## Run the webapp
./arch_ubuntu run

```

Upon completion `./arch_ubuntu run` returns:  
`Starting development sever at http://<ip>:<port>/`  
you can run the webapp using the returned URL.

To test all the features you will need to sign up with a false account and log in. Then you will be directed to a page where you need to upload an xml file that is the output of the kernel, any valid pathway file will do (there's an example xml file in app/static/ ). When you upload a file that will be parsed to json and display the information in a reactive graphical interface. This journey will have shown you every major feature.

*All packages installed by `./arch_ubuntu install` are inside of a virtual env, so it will not conflict with your existing development setup.*

###After Install
You need to upload a pathway xml file to test the interface. That means you need to do 3 steps

   - Register a user (using a dummy email and a password over 6 char)
   - Upload a pathway (An example file is provided in app/static/xml in the project)
   - Then you will see the interface

This allows you to test all the features from user system, xml parsing to the actual interface the patients will use.

##Testing

Using Django TestCase module built on top of Python’s  unittest module.

To run the tests run `./ubuntu test`

### Core
`app/core/tests.py`  

Tests the login form. Tests that the file uploader handles incorrect file formats (non XML) and invalid XML files (with incorrect syntax) correctly. Also test the status code of each response appropriately.

### Processes
`app/processes/tests.py`

Tests the XML to JSON conversion. Also tests the status codes of each response appropriately.

## Feature Listing

### Authentication - Completed

Uses Django AllAuth library.  
Includes password recovery, signing up, logging in and logging out.  
There’s no need to confirm an email. Password must be 6 characters or longer but no symbol restrictions apply.

To try it out:

Sign Up | Sign In | Sign Out | Password Recovery
------- | -------|-----|-----------------
`/accounts/signup/` | `/accounts/login/` | `/accounts/logout/` | `/accounts/password/reset/`

On the homepage when not logged in click on the "Use Local Login" button to check these features.

###OpenEMR Integration - Completed

The default screen will be an OpenEMR login screen, that makes a integrated login possible if an OpenEMR instance is available. At time of writing we used a instance running at `http://openemr.kev.sh/`, this makes available a user with name `demo` and password also `demo`. The choice of email is arbitrary for the first login but will be associated with this account locally for future logins.


### Pathway Listing - Completed

On Login you will either see your pathway view or an upload screen. If you are on the upload screen you can upload an example XML, the project provides one in `arch/app/static/xml/pathways.xml`.

####Process Structure / Process State / XML Parser

The list of pathways is extracted from the XML process table. Then the pathway structure is extracted from each and finally the action states are extracted. This information is then converted to JSON using Python and it’s built-in capabilities.

See `arch/app/processes/views.py` for the XML to JSON conversion.

### Pathway View (Graph View) - Completed

####Graph Layout
The graph is read top down. The top cell beginning of a sequence of actions. A branch is represented by two or more sequences of cells appearing beside each other.

####Pan / Zoom
Pan around the view by scrolling vertically or horizontally. Zoom into a cell by clicking it and zoom out by going back a page.

####Click to Display Metadata
The metadata of an action (it’s description and status) will be shown once you click on the cell and it is in it’s most nested position.

####Testing

There are several tests set up on Jenkins and these infer several tests in the Django apps we use. They are not tailored to ours but show the mechanics of the brought in apps work fine.

###Mobile Friendly

####Tablets
Full tablet support

####Phones
Full phone support
