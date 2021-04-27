.DEFAULT_GOAL := run

IMAGE_NAME := gcr.io/buffer-data/cricket:latest

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: get-model
get-model:
	curl -LJ https://github.com/unitaryai/detoxify/releases/download/v0.1-alpha/toxic_original-c1212f89.ckpt -o model.ckpt

.PHONY: dev
dev: build
	docker run -it -v $(PWD):/app -p 8000:8000 --rm $(IMAGE_NAME) /bin/bash

.PHONY: run
run:
	uvicorn main:app --reload

.PHONY: docker-run
docker-run: build
	docker run -it -p 80:80 --rm $(IMAGE_NAME)

.PHONY: docker-push
docker-push: build
	docker push $(IMAGE_NAME)

.PHONY: deploy
deploy: docker-push
	gcloud beta run services replace service.yaml --platform managed --region us-central1
