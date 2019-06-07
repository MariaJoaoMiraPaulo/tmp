.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "Available tasks:"
	@echo "    container         prepare container to run"
	@echo "    run               run container"
	@echo "    stop              stop container"
	@echo "    watch             watch container logs"
	@echo ""

container:
	@echo "-- CREATING IMAGE --"
	@./docker.sh build

run:
	@echo "-- REMOVE CONTAINER --"
	@./docker.sh remove
	
	@echo "-- START NEW CONTAINER --"
	@./docker.sh run

stop:
	@echo "-- STOP CONTAINER --"
	@./docker.sh stop

watch:
	@cd docker
	@docker container logs -f subject_analyzer_container
