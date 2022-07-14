venv:
	sudo apt install -y python3-venv
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	deactivate

venv-run:
	source venv/bin/activate
	python main.py