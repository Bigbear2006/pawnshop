all: run

run:
	docker-compose up --build -d

info:
	echo "create .env"
	echo "create directory backend/logs"
	echo "curl -o backend/media/branches/default.png https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPL8aJ2mzcUwNoGJomClUsUgXYPkRr6ZRRX-PWlWlVx1BqpttEpg-ThcskOVE5nK4KGQo&usqp=CAU"

logs:
	docker-compose logs -f bot

restart:
	docker-compose restart bot

dump:
	docker-compose exec django python manage.py dumpdata core.branch --indent 2 -o fixtures/branches.json
	docker-compose exec django python manage.py dumpdata core.spendoption --indent 2 -o fixtures/spend_options.json
	docker-compose exec django python manage.py dumpdata core.onlineevaluationguide --indent 2 -o fixtures/online_evaluation_guides.json
	docker-compose exec django python manage.py dumpdata core.oursite --indent 2 -o fixtures/our_sites.json

load:
	docker-compose exec django python manage.py loaddata $(FILES)

keygen:
	python -c "import secrets; print(secrets.token_urlsafe(50))"
