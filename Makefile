IMAGE_NAME=embeddedsearch
build_image: ## Build the docker image
	docker build -t $(IMAGE_NAME) . ;

docker_run: ## Run the docker image
	docker run --rm -v /tmp/indexes:/tmp/indexes  -p 8000:8000 $(IMAGE_NAME);

pb_codegen: ## Generate the protobuf code
	protoc --proto_path=./protos --python_out=./embeddedsearch/pb protos/documents.proto ;

run: ## Run the app locally
	python embeddedsearch/main.py

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//';
