IMAGE := socker_reuse
HERE := `pwd`

build:
	docker build -t $(IMAGE) .

run-fd:
	docker run -it -v $(HERE):/code $(IMAGE) python /code/driver.py fd

run-addr:
	docker run -it -v $(HERE):/code $(IMAGE) python /code/driver.py addr
