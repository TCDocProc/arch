<!--[![Build Status](http://jenkins.kev.sh/job/DjangoMasterUnitTests/badge/icon)](http://jenkins.kev.sh/job/DjangoMasterUnitTests/)--> 

##TCDocProc

A user-friendly interface for presenting care pathways for a single patient using the PML language. It includes easy integration with working OpenEMR installations and a modern interactive interface for displaying the information.

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

###Ubuntu (Without Using Docker)

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

Upoun completion `./arch_ubuntu run` returns:  
`Starting development sever at http://<ip>:<port>/`  
you can run the webapp using the returned URL.

*All packages installed by `./arch_ubuntu install` are inside of a virtual env, so it will not conflict with your existing development setup.*

##Usage Instructions (After Installed & Running)
If you are not logged in you will be presented with two login options, OpenEMR login or Local Sample User Login.       

###OpenEMR Login
Using the OpenEMR approach your pathways will be automatically retrieved for you and presented using our patient interface.
The login credentials are prefilled and you can simply just login.

####Proc Table Placement
$file_path is the variable to change in the tcd_doc_proc.php file to make the xml file your targeting configurable.

Place the tcd_doc_proc.php file in the root OpenEMR web folder, usually /var/www/site, but may vary depending on your installation.

###Local Users Login
Local users are accounts created on your system. You can use the sample one or create your own (to create your own look at the Authentication Feature).
To use the Sample one click on "Sample Sign-in" which will log you in with a sample user.

After login with a local user you're presented with two buttons to either upload your own Pathway XML file, or use a Sample file provided by us if you don't have access to one. After this process your pathways presented using our patient interface. You may upload a different XML file later on by pressing the button in the header called "Upload New XML Pathway".

This allows you to test all the features from the user system, XML parsing to the actual interface the patients will use.

##Testing

Our tests are written using the Django TestCase module built on top of Python’s unittest module.

To run the tests run `./arch_ubuntu test`. This runs all other python tests listed below.

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

Note: These features are only for local users, not OpenEMR users. They are here to demonstrate the backend works and also so you can play around with the user system we built directly.

The reccomended usage is the OpenEMR user login or Sample Local User that is provided on the homepage.

However if you want to change local users, these are the urls to use.

Sign Up | Sign In | Sign Out | Password Recovery
------- | -------|-----|-----------------
`/accounts/signup/` | `/accounts/login/` | `/accounts/logout/` | `/accounts/password/reset/`

###OpenEMR Integration - Completed

The default home screen when not logged is a screen that allows you to login using OpenEMR patient credentials. Currently we use an instance running at `http://openemr.kev.sh/`, to login to that URL use the doctors username and password 'demo'. Note that those details are useless on our system as they are for a doctor and our system is for patients.

Note that to install our system with any running OpenEMR system all you need to do is drop in our PHP file (OpenEMR_integration/TCD_Doc_proc.php) into the OpenEMR system to create an endpoint. And then in our settings.py file change the OpenEMR endpoint to the one you just created.

### Pathway Listing - Completed

On Login you will either see your pathway view or an upload screen. If you are on the upload screen you can upload an example XML, the project provides one in `arch/app/static/xml/pathways.xml`.

####Process Structure / Process State / XML Parser - Completed

The list of pathways is extracted from the XML process table. Then the pathway structure is extracted from each and finally the action states are extracted. This information is then converted to JSON using Python and it’s built-in capabilities.

See `arch/app/processes/views.py` for the XML to JSON conversion.

### Pathway View (Graph View) - Completed

###Task List - Completed
Early Feature agreed upoun. Now it is included in the graph view as agreed, which is itself a list of active and inactive tasks.

####Graph Layout - Completed
The graph is read top down. The top cell beginning of a sequence of actions. A branch is represented by two or more sequences of cells appearing beside each other.

####Graph View Refinement - Completed
There are many graph view refinements which most are listed below

*Minimap*

Once you have selected a specific Pathway you will see a Minimap in the left panel on the screen.   
If you don't see one, press the hamburger button in the top left of the screen to toggle the left panel to show.   
As you nest into the Pathways structure, you will see the Minimap on the left update to correspond to your current position in the structure. The section you are out is visible while everything else is slightly dimmed out. To return to the root of the structure simply press on the Minimap.

*Legend*

Show the left panel (if not already visible) by pressing the hamburger button in the top left.   
The legend shows what state each colour corresponds to.   

*Active Shortcut*

To go directly to the active step in the Pathway, press the button in the left panel called 'Go to Active Step'. This button only shows up if you're in a Pathway and it has an active step somewhere in it.

*Breadcrumbs for Better Navigation*

These help you know how deep into the tree you have travelled. And also hop back to any point in that tree.

####Pan / Zoom
Pan around the view by scrolling vertically or horizontally. Zoom into a cell by clicking it and zoom out by going back a page.

####Click to Display Metadata
The metadata of an action (it’s description and status) will be shown once you click on the cell and it is in it’s most nested position.

###Mobile Friendly

The easiest way to test these is to use Firefox as the browsers and go into Tools > Web Developer > Responsive Design View and use that tool to check out the various sizes. A page refresh is often necessary after changing the page size to see the affects.

####Tablets
Full tablet support

####Phones
Full phone support. The only important change here is you can log out using the side menu now to free up the navigation bar space.

###Shepherding - Completed
Upon seeing our patient interface for the very first time the user will be presented with a series of instructional popups that points at a certain part of the interface and guide the user through using it. During this process everything on the screen, except for the part of interest for the current step of the instructions, are greyed out and non-interactable.   
This further aids the user to see exactly what part of the interface we're teaching them about. Using cookies we ensure the Shepherding only happens once for each browser. The purpose of this is to familiarise the user with the key components of the interface.

We use an open-source HubSpot library called [Shepherd](https://github.com/HubSpot/shepherd) to achieve this. However the part that handles greying out parts of the screen and stopping interaction is done by us and not HubSpot's library.

If you want to show the tutorial again but it's not your first time visiting the page, you can simple trigger it again using the 'Show Tutorial' button in the top bar on screen.

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

