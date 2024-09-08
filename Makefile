IMAGE_NAME=embeddedsearch
build_image: ## Build the docker image
	docker build -t $(IMAGE_NAME) .

docker_run: ## Run the docker image
	docker run --rm -v /tmp/xapian_index:/tmp/xapian_index  -p 8000:8000 $(IMAGE_NAME)

run: ## Run the app locally
	python embeddedsearch/app.py

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
