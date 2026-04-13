.PHONY: run stop test

run: stop
	uv run python main.py

stop:
	@lsof -ti :8888 | xargs kill -9 2>/dev/null || true

test:
	uv run python -m tests.test_demo
