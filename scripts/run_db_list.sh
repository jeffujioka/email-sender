#!/usr/bin/env bash

docker-compose exec email-sender-db psql -U postgres -c '\l'
