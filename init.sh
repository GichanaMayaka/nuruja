#!/bin/sh
export ENV=dev && exec gunicorn --bind 0.0.0.0:8000 --forwarded-allow-ips='*' wsgi:app