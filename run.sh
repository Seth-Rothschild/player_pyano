#!/bin/bash


python3 player_pyano/app.py & yarn start
lsof -ti :3001 | xargs kill
