tests:
	docker-compose -f docker-compose-ci.yml build
	docker-compose -f docker-compose-ci.yml up -d db
	docker-compose -f docker-compose-ci.yml run consume pytest --cov=.
	docker-compose -f docker-compose-ci.yml run produce pytest --cov=.