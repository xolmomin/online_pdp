to_req:
	uv pip compile pyproject.toml --output-file requirements.txt

build:
	docker build -t online_pdp .

create_con:
	docker run -p 8000:8000 online_pdp

mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

msg:
	python3 manage.py makemessages -l uz -l en

compile_msg:
	python3 manage.py compilemessages -i .venv

fixture:
	python3 manage.py loaddata blogs course interviews lesson section