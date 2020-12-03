.DEFAULT_GOAL := run

IMAGE_NAME := gcr.io/buffer-data/cricket:latest

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: get-model
get-model:
	curl -LJ https://github.com/unitaryai/detoxify/releases/download/v0.1-alpha/toxic_original-c1212f89.ckpt -o model.ckpt

.PHONY: run
run: build
	docker run -it -p 80:80 --rm $(IMAGE_NAME)

.PHONY: dev
dev: build
	docker run -it -v $(PWD):/app -p 80:80 --rm $(IMAGE_NAME) /bin/bash /start-reload.sh

.PHONY: bash
bash: build
	docker run -it -v $(PWD):/app -p 80:80 --rm $(IMAGE_NAME) /bin/bash

.PHONY: push
push: build
	docker push $(IMAGE_NAME)

.PHONY: deploy
deploy: push
	gcloud beta run --platform managed services replace service.yaml
