# Airflow 101

[![Build Status](https://travis-ci.org/python-jitsu/airflow101.svg?branch=master)](https://travis-ci.org/python-jitsu/airflow101)

Материал курса по работе с Airflow 101.

Подробнее про курс можно почитать на нашем сайте: <https://airflow101.python-jitsu.club/>.

## Коротко о курсе

Трёхнедельный интенсив с кучей самостоятельной работы для тех, кто
хочет выучить Airflow.

В этом репо есть весь материал курса, кроме самого ценного – фидбека
на домашние задания.

## Honor code

Мы соблюдаем
[кодекс чести Стенфордского университета](https://communitystandards.stanford.edu/policies-and-guidance/honor-code).

Ему почти 100 лет, он короткий и понятный. Мы не читерим, не помогаем
читерить другим и всё такое.

## Материалы

### 1. Intro: Airflow, DAG, scheduler

#### Challenge

1. Арендовать сервер, разрешить вход по ssh ключу для оргов (ключ будет в чате).
1. Развернуть на сервере Airflow, спрятанный за basic auth.
1. Написать и выкатить DAG, который ходит в
  [апишку Яндекса](https://yastat.net/s3/milab/2020/covid19-stat/data/data_struct_10.json?v=timestamp),
  тянет оттуда данные по коронавирусу и кладет их в .csv файлик, который можно скачать.

Требования к DAG:

- Запускается каждый день в 12:00 по Москве.
- Тянет все данные до текущего момента.
- Складывает данные по России.
- Колонки в csv: date, region, infected, recovered, dead.

#### Материалы для изучения

- [Airflow Quick Start](https://airflow.apache.org/docs/stable/start.html).
- [Airflow Concepts](https://airflow.apache.org/docs/stable/concepts.html).
- [Airflow tutorial](https://airflow.apache.org/docs/stable/tutorial.html).
- [Airflow Scheduling & Triggers](https://airflow.apache.org/docs/stable/scheduler.html).
- [Getting started with Apache Airflow](https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b).
- [Nginx – Serving Static Content](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/).

### 2. Источники, сенсоры и хуки

#### Challenge

1. Сделать DAG из нескольких шагов, собирающий данные по заказам, проверяющий
   статусы транзакций через API и складывающий результат в базу данных
1. Данные по заказам брать в виде csv-файла
   [отсюда](https://airflow101.python-jitsu.club/orders.csv)
1. Данные по статусам транзакций хранятся в виде json
   [тут](https://api.jsonbin.io/b/5ed7391379382f568bd22822)
1. Данные о товарах и пользователях живут в PostgreSQL БД (доступ в тг чате).
1. Результаты складывать в другую PostgreSQL БД (доступ к ней будет у вас в
   личке). Именно в ней должен лежить финальный датасет.

Требования к DAG:

- На каждый источник должен быть один оператор.
- Повторные выполнения DAG должны обновлять имеющиеся данные. То есть,
  если статус транзакции изменился на "оплачен", то это должно быть
  отражено в датасете.
- Из любого источника могут приходить грязные данные. Делайте чистку:
  удаляйте дубли, стрипайте строки, проверяйте на null/None.
- Логин/пароль для доступа в postgres базу надо получить у оргов
  (dbname совпадает с вашим логином).
- Прежде чем писать в постгрес, надо убедиться, что там есть схема
  и таблица.
- Вы можете использовать pandas, но вообще в благородных домах
  pandas не тянут "в продакшен".
- Финальный датасет содержит следующие колонки: `name`, `age`,
  `good_title`, `date`, `payment_status`, `total_price`, `amount`, `last_modified_at`.

#### Материалы для изучения

Дополнительные ссылки на почитать к сегодняшнему вебинару:

- [Пример конфига nginx](https://airflow.apache.org/docs/stable/howto/run-behind-proxy.html)
- [Как безопасно хранить пароли в connection](https://airflow.apache.org/docs/stable/howto/secure-connections.html)
- [Как запустить airflow как сервис](https://airflow.apache.org/docs/stable/howto/run-with-systemd.html)
- Все говорят, что динамические даги делать нельзя, а
  [тут](https://blog.pythian.com/creating-dynamic-tasks-using-apache-airflow/)
  говорят что можно (подумайте какие у этого могут быть проблемы).
- Посмотреть на примеры пайплайнов и организацию кода:
  [airflow в cloud compose](https://blog.freetrade.io/how-we-simplified-our-data-pipeline-54f377fad3c),
  [о том как дробить даг на таски и операторы](https://gtoonstra.github.io/etl-with-airflow/platform.html),
  [как собирать пайплайн из простых конфигов](https://humansofdata.atlan.com/2018/08/airflow-meta-data-engineering-disha/).

## Contributing

Хотя это материалы конкретного курса, мы будем рады, если вы захотите добавить
материала по темам курса, дать ссылки на более актуальные статьи или полезные
инструменты, которые мы не рассмотрели. Если вы поправите ошибку или неточность –
мы тоже будем рады.
