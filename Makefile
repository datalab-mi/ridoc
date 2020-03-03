# include .env file
include .env

# this is usefull with most python apps in dev mode because if stdout is
# buffered logs do not shows in realtime
PYTHONUNBUFFERED=1
#export

.env:
	cp .env.sample .env

venv:
	python3 -m venv venv;
	venv/bin/pip3 install -U -r requirements.txt;

up: venv
	venv/bin/python3 run.py
