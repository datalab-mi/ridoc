# include .env file
#include .env

# this is usefull with most python apps in dev mode because if stdout is
# buffered logs do not shows in realtime
PYTHONUNBUFFERED=1
#export

venv:
	python3 -m venv venv;
	venv/bin/pip install -U -r requirements.txt;


up:
	venv/bin/python run.py
