import requests
#from rich import print
import json
from typing import List

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

    def get_stargazers_logins(self) -> List[str]:
        stargazers_api_url = f'{self.url}/stargazers'
        response = requests.get(stargazers_api_url, timeout=3)
        return [stargazer['login'] for stargazer in response.json()]

    def as_dict(self):
        return {
            'stars_count': self.stars,
            'repo_name': self.full_name,
            'stargazers': self.get_stargazers_logins(),
        }


class GithubStarsReportOperator(BaseOperator):
    @apply_defaults
    def __init__(self, repo_url: str, stars_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = repo_url
        self.repo_info = GithubRepoInfo(repo_url=self.url)

        self.stars_filename = stars_filename

    def execute(self, *args, **kwargs):
        self.repo_info.fetch()
        stargazers = self.repo_info.get_stargazers_logins()
        print(f'Repo {self.repo_info.full_name} has {self.repo_info.stars} stars: {stargazers}')

        with open(self.stars_filename, 'w') as fp:
            json.dump(self.repo_info.as_dict(), fp)

        print(f'Dumped info as {self.stars_filename}')


class GithubStarsIncrementSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, repo_url: str, stars_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = repo_url
        self.repo_info = GithubRepoInfo(repo_url=self.url)
        self.starting_stars = None
        self.stars_filename = stars_filename

    def read_stars(self):
        with open(self.stars_filename) as fp:
            repo_info = json.load(fp)
        self.starting_stars = repo_info['stars_count']

    def poke(self, *args, **kwargs):
        if self.starting_stars is None:
            self.read_stars()

        print(f'poking {self.url}')
        self.repo_info.fetch()
        return self.repo_info.stars > self.starting_stars


class GithubNotifyNewStargazersOperator(BaseOperator):
    @apply_defaults
    def __init__(self, repo_url: str, stars_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = repo_url
        self.repo_info = GithubRepoInfo(repo_url=self.url)
        self.stars_filename = stars_filename

    def execute(self, *args, **kwargs):
        with open(self.stars_filename) as fp:
            old_repo_info = json.load(fp)
        starting_stargazers = old_repo_info['stargazers']
        print('old stargazers', starting_stargazers)

        current_stargazers = self.repo_info.get_stargazers_logins()
        print('current stargazers', current_stargazers)

        new_stargazers_urls = [
            f'https://api.github.com/users/{stargazer}/events/public'
            for stargazer in current_stargazers if stargazer not in starting_stargazers
        ]
        print(f'New stargazers: {new_stargazers_urls}')


default_args = {
    'owner': 'Me',
    'start_date': days_ago(2),
    'stars_filename': '/tmp/stars_and_stargazers_info.json',
    'repo_url': BASE_API_URL,
}

dag = DAG(dag_id='2_stargazer_getter', schedule_interval='@once', default_args=default_args)

get_stars = GithubStarsReportOperator(task_id='get_stars', dag=dag)
wait_for_stars = GithubStarsIncrementSensor(task_id='wait_for_stars', poke_interval=10, dag=dag)
get_new_stargazers = GithubNotifyNewStargazersOperator(task_id='get_new_stargazers', dag=dag)

all_success = DummyOperator(task_id='all_success', dag=dag)

get_stars >> wait_for_stars >> get_new_stargazers >> all_success
