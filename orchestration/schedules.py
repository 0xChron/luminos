from dagster import ScheduleDefinition
from .jobs import daily_pipeline_job

daily_schedule = ScheduleDefinition(
    name="daily_pipeline_schedule",
    job=daily_pipeline_job,
    cron_schedule="0 1 * * *",  # 1 am utc+8
    execution_timezone="Asia/Singapore",
    description="daily ingestion and transformation pipeline at 1 am sgt"
)