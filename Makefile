.PHONY: image

IMAGE_NAME ?= codeclimate/codeclimate-mypy

image:
	docker build --rm -t $(IMAGE_NAME) .
