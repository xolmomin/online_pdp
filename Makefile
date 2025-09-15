to_req:
	uv pip compile pyproject.toml --output-file requirements.txt

build:
	docker build -t online_pdp .

create_con:
	docker run -p 8000:8000 online_pdp

mig_local:
	source .env
	python3 manage.py makemigrations
	python3 manage.py migrate
