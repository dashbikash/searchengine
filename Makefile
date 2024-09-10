IMAGE_NAME=embeddedsearch
build_image: ## Build the docker image
	docker build -t $(IMAGE_NAME) . ;

docker_run: ## Run the docker image
	docker run --rm --name $(IMAGE_NAME) -v /tmp:/tmp  -p 8000:8000 $(IMAGE_NAME);

pb_codegen: ## Generate the protobuf code
	protoc --proto_path=./protos --python_out=./embeddedsearch/pb protos/documents.proto ;

run: ## Run the app locally
	python embeddedsearch/main.py
	
dummy_index: ## Index dummy data
	docker exec  -it $(IMAGE_NAME) python3 embeddedsearch/script.py i

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//';
