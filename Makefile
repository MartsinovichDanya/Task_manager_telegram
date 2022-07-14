venv:
	sudo apt-get install python3.8-venv
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	deactivate

venv-run-tm:
	python3 bot.py

venv-run-ph:
	python3 pravo_help.py