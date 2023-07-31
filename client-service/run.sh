#!/bin/bash

sleep 5
python ./init_db.py
gunicorn -w 1 -b 0.0.0.0:3000 "app:create_app()"
