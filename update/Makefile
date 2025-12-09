ACTIVATE = . conda/etc/profile.d/conda.sh && conda activate
TARGETS  = env dev format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	./env

dev:
	EAGLE_DEV=1 ./env

format:
	@./format

lint:
	ruff check .

test: lint typecheck unittest

typecheck:
	mypy --install-types --non-interactive .

unittest:
	pytest --cov .
