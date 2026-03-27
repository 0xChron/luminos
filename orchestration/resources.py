from dagster_dbt import DbtCliResource
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DBT_PROJECT_DIR = PROJECT_ROOT / "transform"

dbt_resource = DbtCliResource(
    project_dir=str(DBT_PROJECT_DIR),
)