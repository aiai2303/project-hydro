#!/usr/bin/bash

gunicorn -b 0.0.0.0:7860 web:app &
python -u main.py