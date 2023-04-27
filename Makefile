install:
	conda create -p env python=3.10 -y
	env/bin/python -m pip install -r requirements.txt

start:
	env/bin/python app.py