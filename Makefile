all: up

up:
	docker compose -f docker-compose.yml up --build -d

down:
	docker compose -f docker-compose.yml down

clean: down
	docker system prune -af

fclean: clean
	docker network prune -f
	docker volume rm $$(docker volume ls -qf dangling=true)

re: down up

.PHONY: all up down clean re