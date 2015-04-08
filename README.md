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

## Run the tests
./arch_ubuntu test

```

Upon completion `./arch_ubuntu run` returns:  
`Starting development sever at http://<ip>:<port>/`  
you can run the webapp using the returned URL.

*All packages installed by `./arch_ubuntu install` are inside of a virtual env, so it will not conflict with your existing development setup.*

##Usage Instructions (After Installed & Running)
If it's your first time or you are not logged in, you will be presented with a login page.   
You have the option of using OpenEMR login or Local login.   
Using OpenEMR your pathways will be automatically retrieved for you and presented using our patient interface.   
Using the local approach allows you to specify your own pathway XML file or use our sample file. 

###OpenEMR
To login using OpenEMR use an arbitrary email address and the username and password that is provided on the webpage. After first login you MUST use the same arbitrary email for future logins as it is associated with this account locally.

###Local
This approach allows you to create a local account by signing up or logging in with your existing local account.

**Creating a new local account**
- Enter an arbitrary email address
- Enter a password (6 characters or more)
- Enter the above password again to verify

After account creation you're presented with two buttons to either upload your own Pathway XML file, or use a Sample file provided by us if you don't have access to one. Similarly this will happen if you login and no pathways are associated with your account, otherwise you will just see your pathways presented using our patient interface.

This allows you to test all the features from user system, XML parsing to the actual interface the patients will use.

##Testing

Using Django TestCase module built on top of Python’s  unittest module.

To run the tests run `./arch_ubuntu test`

### Core
`app/core/tests.py`  

This tests the login form. Tests that the file uploader handles incorrect file formats (non XML) and invalid XML files (with incorrect syntax) correctly. Also tests the status code of each response appropriately.

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

The default home screen when not logged is a screen that allows you to login using OpenEMR patient credentials. Currently we use an instance running at `http://openemr.kev.sh/`, to login to that URL use the doctors username and password 'demo'. Note that those details are useless on our system as they are for a doctor and our system is for patients.

Note that to install our system with any running OpenEMR system all you need to do is drop in our PHP file (OpenEMR_integration/TCD_Doc_proc.php) into the OpenEMR system to create an endpoint. And then in our settings.py file change the OpenEMR endpoint to the one you just created.

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

###Mobile Friendly

The easiest way to test these is to use Firefox > Tools > Web Developer > Responsive Design View and use that tool to check out the various sizes. A page refresh is often necessary after changing the page size to see the affects.

####Tablets
Full tablet support

####Phones
Full phone support

###Shepherding - Completed
Upon seeing our patient interface for the very first time the user will be presented with a series of instructional popups that will point at elements of interest in the interface and guide them through using the system. This will not show up the next time the user returns. The purpose of this is to familiarise the user with the key components of the interface.
