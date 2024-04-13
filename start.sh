#!/usr/bin/bash

gunicorn -b 0.0.0.0:8080 web:app &
python -u main.py