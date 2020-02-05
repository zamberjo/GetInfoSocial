#!/bin/bash

git pull origin master;
# docker-compose -f stack-service.yaml -f stack-service.armv8.yaml -p getinfo up -d --build --force-recreate;
getinfo_restart;
clear;
# docker-compose -f stack-service.yaml -f stack-service.armv8.yaml -p getinfo logs -f getinfo;
getinfo_logs;
