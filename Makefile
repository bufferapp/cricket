.DEFAULT_GOAL := run

IMAGE_NAME := gcr.io/buffer-data/cricket:latest

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run: build
	docker run -it --env-file .env -p 80:80 --rm $(IMAGE_NAME)

.PHONY: dev
dev: build
	docker run -it --env-file .env -v $(PWD):/app -p 80:80 --rm $(IMAGE_NAME) /bin/bash /start-reload.sh

.PHONY: push
push: build
	docker push $(IMAGE_NAME)

.PHONY: deploy
deploy: push
	gcloud run deploy cricket --image $(IMAGE_NAME) --platform managed --region us-central1