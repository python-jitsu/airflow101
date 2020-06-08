from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from github_interactions.operators import (
    GithubStarsReportOperator,
    GithubNotifyNewStargazersOperator
)
from github_interactions.sensors import GithubStarsIncrementSensor


default_args = {
    'owner': 'Me',
    'start_date': days_ago(2),
    'stars_filename': '/tmp/stars_and_stargazers_info_aoeunhaoneuh.json',
    'repo_url': "https://api.github.com/repos/python-jitsu/airflow101",
    'token': '3-да-конечно-прям-так-взял-и-дал-токен-5',
}


def make_dage(default_args)
    dag = DAG(dag_id='4_stargazer_emails_nice', schedule_interval='@once', default_args=default_args)

    get_stars = GithubStarsReportOperator(task_id='get_stars', dag=dag)
    wait_for_stars = GithubStarsIncrementSensor(task_id='wait_for_stars', poke_interval=10, dag=dag)
    get_new_stargazers = GithubNotifyNewStargazersOperator(task_id='get_new_stargazers', dag=dag)

    all_success = DummyOperator(task_id='all_success', dag=dag)

    get_stars >> wait_for_stars >> get_new_stargazers >> all_success

dag = make_dag(default_args)
