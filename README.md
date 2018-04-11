# Web Demo for MAttNet

## Introduction
This repository is for setting up the [web demo of MAttNet](http://vision2.cs.unc.edu/refer/).
Its design basically follows the great repo [Grad-CAM](https://github.com/Cloud-CV/Grad-CAM/).

## How to use
0) Set up environments: 
- Ubuntu environment
```bash
sudo apt-get install nginx  # we use nginx (rather than apache) for using websocket
sudo apt-get install uwsgi  # we use uwsgi for web service
sudo apt-get install -y rabbitmq-server  # pika in python, for publish and request
sudo apt-get install redis-server  # used for websocket
```
- Virtual environment
```bash
# set up virtualenv
virtualenv demoenv
pip install -r requirements.txt
```
```bash
# activate this environement
source demoenv/bin/activate
```
1) Start django project:
```
django-admin startproject demo .
```
2) Add an app called `refer`
```
python manage.py startapp refer
```
3) Set up models and build database
- Edit `refer/models.py`, adding the keys/contents we want in the database.
- Register database
```
python manage.py makemigratoins refer
python manage.py sqlmigrate refer 0001
python manage.py migrate
```
4) Symlink MAttNet repo and model here!
```bash
ln -s /playpen1/licheng/Documents/MattNet2s .  # we use MAttNet2S's refcoco+genome model
```

## Run the demo (env activated)
- prerequisite:
```bash
./manage.py collectstatic  # collect all static imgs
sudo ln -s refer_demo_nginx.conf /etc/nginx/sites-available/refer_demo_nginx.conf  # symlink nginx setting
sudo service nginx restart  # restart nginx service
sudo service rabbitmq-server start  # start rabbitmq (for using pika), everytime after server rebooting
```
- screen 1:
```bash
./demoenv/bin/uwsgi --ini uwsgi.ini  # have to use pip installed uwsgi somehow...
```
- screen 2:
```python
CUDA_VISIBLE_DEVICES=x python worker_comprehension.py  # run comprehension callback, waiting for request from refer/sender
```
- screen 3:
```bash
daphne demo.asgi:channel_layer --port 9000  # have to use asgi for websocket
```
- screen 4:
```python
python manage.py runworker  # run this demo
```

## Mechanism
- We use jQuery's `ajax` and `post` to get the query image and expression, use `pika` for publishing/requesting a comprehension job, and use `websocket` to get model's response reflecing its results on web.

## Database reset
- In order to check database, install ``apt-get install sqlite3 libsqlite3-dev``. If for some reason we need to reset database, run:
```
python manage.py flush
python manage.py makemigrations refer
python manage.py sqlmigrate refer 0001
python manage.py migrate
```

## TODO
- Generation demo
- Robot grasping demo