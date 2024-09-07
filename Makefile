IMAGE_NAME=embeddedsearch
build_image:
	docker build -t $(IMAGE_NAME) .

docker_run:
	docker run --rm -v /tmp/xapian_index:/tmp/xapian_index  -p 8000:8000 $(IMAGE_NAME)

help:
	@echo "build_image: build docker image"
	@echo "docker_run: run docker image"
	@echo "help: show this message"