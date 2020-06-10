#!/usr/bin/env bash

chown -R nginx:nginx web
pip install bottle==0.12.18
python -u sender.py