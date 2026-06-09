.PHONY: backfill-solar backfill-weather dbt-run dbt-test dbt-build dbt-docs view airflow docker-build down

START_DATE ?= 2026-03-15
END_DATE ?= 2026-03-30

backfill-solar:
	uv run python -m ingest.jobs.backfill_solar_job \
		--start-date $(START_DATE) \
		--end-date $(END_DATE)

backfill-weather:
	uv run python -m ingest.jobs.backfill_weather_job \
		--start-date $(START_DATE) \
		--end-date $(END_DATE)

dbt-run:
	uv run dbt run --project-dir transform --target dev

dbt-test:
	uv run dbt test --project-dir transform --target dev

dbt-build:
	uv run dbt build --project-dir transform --target dev

dbt-docs:
	uv run dbt docs serve --project-dir transform --target dev

view:
	duckdb luminos.duckdb -ui

airflow:
	docker-compose up airflow-init

docker-build:
	docker-compose build && docker-compose up -d

down:
	docker-compose down -v