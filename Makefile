compose-start:
	@docker-compose up --build -d

compose-stop:
	@docker-compose down -v --remove-orphans

commit:
	docker-compose exec db alembic revision --autogenerate -m "$$(name)"

migrate:
	@docker-compose exec db alembic upgrade head

downgrade:
	@docker-compose exec db alembic downgrade -1
