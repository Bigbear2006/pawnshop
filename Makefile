all: run

run:
	docker-compose up --build -d

info:
	echo "create .env"
	echo "create directory backend/logs"
	echo "curl -o backend/media/branches/default.png https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPL8aJ2mzcUwNoGJomClUsUgXYPkRr6ZRRX-PWlWlVx1BqpttEpg-ThcskOVE5nK4KGQo&usqp=CAU"

logs:
	docker-compose logs -f

dump:
	docker-compose exec django python manage.py dumpdata core.branch core.spendoption core.onlineevaluationguide --indent 2 -o data.json

load:
	docker-compose exec django python manage.py loaddata data.json

keygen:
	python -c "import secrets; print(''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)))"
