.PHONY: build up down logs create-test-data install-local

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs -f

create-test-data:
	cd backend && pip3 install openpyxl -q && python3 create_test_data.py

install-local:
	cd backend && pip3 install -r requirements.txt
	cd frontend/track_a && pip3 install -r requirements.txt
	cd frontend/track_b && pip3 install -r requirements.txt
