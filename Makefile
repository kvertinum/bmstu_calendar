compose-start:
	@docker-compose up --build -d

compose-stop:
	@docker-compose down -v --remove-orphans

commit:
	docker-compose exec app alembic revision --autogenerate -m "$$(name)"

migrate:
	@docker-compose exec app alembic upgrade head

downgrade:
	@docker-compose exec app alembic downgrade -1
