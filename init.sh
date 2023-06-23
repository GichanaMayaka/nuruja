#!/bin/sh
export ENV=dev && exec gunicorn --bind 0.0.0.0:8000 wsgi:app --forwarded-allow-ips='*'