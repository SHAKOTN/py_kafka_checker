tests:
	docker-compose -f docker-compose-ci.yml build
	docker-compose -f docker-compose-ci.yml up -d db
	sleep 10
	docker-compose -f docker-compose-ci.yml run consume pytest --cov=.
	docker-compose -f docker-compose-ci.yml run produce pytest --cov=.

run_production:
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up