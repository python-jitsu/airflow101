from datetime import timedelta
import os
import time
import random

from airflow.models import DAG
from airflow.exceptions import AirflowException
from airflow.utils.dates import days_ago

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from alerts import TelegramAlertHelper


def nice_task():
    #if random.choice([0, 0, 0, 0, 0, 1]) == 1:
    #    raise AirflowException('На самом деле нет, всё плохо')
    time.sleep(10)
    print('Всё ещё не очень хорошо')
    time.sleep(10)
    print('Всё ещё не очень хорошо')
    time.sleep(10)
    print('Всё ещё не очень хорошо')
    time.sleep(10)
    print('Всё хорошо')

token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')

alert_helper = TelegramAlertHelper(token, chat_id)


default_args = {
    'depends_on_past': False,
    'start_date': days_ago(7),
    'email': 'never@call.me',
    'on_success_callback': alert_helper.on_success_callback,
    'on_retry_callback': alert_helper.on_retry_callback,
    'on_failure_callback': alert_helper.on_failure_callback,
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
    'sla_miss_callback': alert_helper.on_sla_miss_callback,
    'sla': timedelta(seconds=20),
}

dag = DAG(
    dag_id='showcase-w5',
    schedule_interval=None,
    default_args=default_args,
)

starting_point = DummyOperator(task_id='start_here', dag=dag)
everything_is_nice_op = PythonOperator(
    task_id='everything_is_nice',
    python_callable=nice_task,
    dag=dag,
)

starting_point >> everything_is_nice_op