ACTIVATE = . conda/etc/profile.d/conda.sh && conda activate
SRCDIRS = eagle
TARGETS = env dev format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	./env

dev:
	EAGLE_DEV=1 ./env

format:
	@echo "=> Formatting code"
	@ruff format $(SRCDIRS)
	@echo "=> Sorting imports"
	@ruff check --select I --fix $(SRCDIRS)

lint:
	ruff check $(SRCDIRS)

test: lint typecheck unittest

typecheck:
	mypy --install-types --non-interactive $(SRCDIRS)

unittest:
	pytest --cov $(SRCDIRS)
