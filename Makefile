LOCAL_MISP_CONNECTOR_DIR := docker/local_misp_connector
TESTS_DIR := docker/tests

### Those macros are for used for code test or setting up a connector for a local MISP.
### To setup a connector to the official datalake MISP, see "Setting up the image" section in README.md

start-connector:
	docker compose -f $(LOCAL_MISP_CONNECTOR_DIR)/docker-compose.yml up --build

clean:
	docker compose -f $(LOCAL_MISP_CONNECTOR_DIR)/docker-compose.yml down --rmi all

test:
	docker compose -f $(TESTS_DIR)/docker-compose.yml down
	docker compose -f $(TESTS_DIR)/docker-compose.yml up --build --abort-on-container-exit
	docker compose -f $(TESTS_DIR)/docker-compose.yml down

