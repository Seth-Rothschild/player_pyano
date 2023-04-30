install:
	conda create -p env python=3.10 -y
	env/bin/python -m pip install -r requirements.txt

build:
	cd frontend && npm run build
	cp -r frontend/build/ templates/

start-frontend:
	## Use to run frontend with live reloading
	## Backend will also need to be running
	cd frontend && npm run dev

start:
	env/bin/python app.py
