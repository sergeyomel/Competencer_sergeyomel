import pendulum
from airflow import DAG
from airflow.decorators import task


with DAG(
    dag_id="parse_hh",
    schedule_interval='@hourly',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["hh_beta"],
) as dag:
    @task(task_id='get_40_pages')
    def hh_task():

        import sys
        sys.path.append('home/borisov/Competencer')

        from src.parsers.hh_parser.get_hh import get_hh

        get_hh()