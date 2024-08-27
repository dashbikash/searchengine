default: help

run: # Run the application
	go run cmd/*.go

build: # Build the application
	go build -o bin/ cmd/*.go

build_image: # Build the docker image
	docker build -t bikashpdash/embedded-search .

help: # Display this help screen
	@awk 'BEGIN {FS = ":.*?# "} /^[a-zA-Z_-]+:.*?# .*$$/ {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)