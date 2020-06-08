import requests
from rich import print
import json

from airflow.models import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.dates import days_ago


BASE_API_URL = "https://api.github.com/repos/python-jitsu/airflow101"


class GithubRepoInfo:
    def __init__(self, repo_url: str):
        self.url = repo_url
        self.info = None

    def fetch(self):
        response = requests.get(self.url, timeout=3)
        self.info = response.json()

    @property
    def stars(self):
        if self.info is None:
            self.fetch()
        return self.info['stargazers_count']

    @property
    def full_name(self):
        if self.info is None:
            self.fetch()
        return self.info['full_name']


class GithubStarsReportOperator(BaseOperator):
    @apply_defaults
    def __init__(self, repo_url: str, stars_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = repo_url
        self.repo_info = GithubRepoInfo(repo_url=self.url)

        self.stars_filename = stars_filename

    def execute(self, *args, **kwargs):
        self.repo_info.fetch()
        print(f'Repo {self.repo_info.full_name} has {self.repo_info.stars} stars')

        with open(self.stars_filename, 'w') as fp:
            json.dump({'stars_count': self.repo_info.stars, 'repo_name': self.repo_info.full_name}, fp)


class GithubStarsIncrementSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, repo_url: str, stars_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = repo_url
        self.repo_info = GithubRepoInfo(repo_url=self.url)

        with open(stars_filename) as fp:
            repo_info = json.load(fp)
        self.starting_stars = repo_info['stars_count']

    def poke(self, *args, **kwargs):
        print(f'poking {self.url}')
        self.repo_info.fetch()
        return self.repo_info.stars > self.starting_stars



default_args = {
    'owner': 'Me',
    'start_date': days_ago(2),
    'stars_filename': '/tmp/stars_info.json',
}

dag = DAG(dag_id='1_stars_printer', schedule_interval='@once', default_args=default_args)

get_stars = GithubStarsReportOperator(task_id='get_stars', repo_url=BASE_API_URL, dag=dag)
wait_for_stars = GithubStarsIncrementSensor(task_id='wait_for_stars', poke_interval=10, repo_url=BASE_API_URL, dag=dag)

all_success = DummyOperator(task_id='all_success', dag=dag)

get_stars >> wait_for_stars >> all_success