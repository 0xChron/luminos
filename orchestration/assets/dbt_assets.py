from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DBT_PROJECT_DIR = PROJECT_ROOT / "transform"
DBT_MANIFEST_PATH = DBT_PROJECT_DIR / "target" / "manifest.json"

@dbt_assets(manifest=DBT_MANIFEST_PATH)
def luminos_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()