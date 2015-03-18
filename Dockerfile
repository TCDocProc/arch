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

run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python python-dev python-setuptools
run apt-get install -y nginx supervisor
run easy_install pip

# install npm
run apt-get install -y curl
run curl -sL https://deb.nodesource.com/setup | bash
run apt-get install -y nodejs

# install bower
run npm install -g bower

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

run mkdir /home/docker/volatile
run mkdir /home/docker/volatile/static

RUN useradd -ms /bin/bash django

# copy the nice dotfiles that dockerfile/ubuntu gives us:
RUN chown -R django:django /home/docker

USER django

# Stop bower using git:// and make it use https:// - for firewalls such as TCD
run git config --global url."https://github.com".insteadOf "git://github.com"

run python /home/docker/code/app/manage.py bower install

USER root

run python /home/docker/code/app/manage.py collectstatic --noinput >/dev/null 2>&1

# sync the database
run cd /home/docker/code/app && \
    python manage.py migrate

cmd ["supervisord", "-n"]
