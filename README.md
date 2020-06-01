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
1. Развернуть на сервере нём Airflow, спрятанный за basic auth.
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
- [Nginx – Serving Static Content](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/)

## Contributing

Хотя это материалы конкретного курса, мы будем рады, если вы захотите добавить
материала по темам курса, дать ссылки на более актуальные статьи или полезные
инструменты, которые мы не рассмотрели. Если вы поправите ошибку или неточность –
мы тоже будем рады.
