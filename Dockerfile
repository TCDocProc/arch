# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ubuntu:12.04

maintainer Dockerfiles

# install PEOS dependencies
run apt-get install -y tcl
run apt-get install -y check
run apt-get install -y libxml2

run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python python-dev python-setuptools
run apt-get install -y nginx supervisor
run easy_install pip

# install npm
run apt-get install -y curl
run curl -sL https://deb.nodesource.com/setup | bash
run	apt-get install -y nodejs

# install yuglify
run npm install -g yuglify

# install bower
run npm install -g bower

# install coffee-script
run apt-get install -y coffeescript

# install sass and compass
run apt-get install -y rubygems
run	gem install compass

# needed by scss compiler
run	gem install json

# install uwsgi now because it takes a little while
run apt-get install -y uwsgi
run apt-get install -y uwsgi-plugin-python

# install nginx
run apt-get update
run apt-get install -y python-software-properties
run apt-get update
run add-apt-repository -y ppa:nginx/stable
run apt-get install -y sqlite3

# install our code
add . /home/docker/code/

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/

# run pip install
run pip install -r /home/docker/code/app/requirements.txt

expose 80

# Stop bower using git:// and make it use https:// - for firewalls such as TCD
run git config --global url."https://github.com".insteadOf "git://github.com"

run mkdir -p /home/docker/volatile/static/components/

run cd /home/docker/code/app && \
 	python ./manage.py bower install jquery#~2.1.1 -- --allow-root && \
	python ./manage.py bower install backbone#~1.1.2 -- --allow-root && \
	python ./manage.py bower install foundation#~5.4.7 -- --allow-root

cmd ["supervisord", "-n"]
