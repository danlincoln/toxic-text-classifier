#!/bin/bash
python -m venv /app/venv
source /app/venv/bin/activate
pip install -r /app/requirements.txt && 
python /app/nltk_libs.py
python /app/manage.py migrate && 
python /app/manage.py runserver --noreload 0.0.0.0:8000