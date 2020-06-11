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

### 3. Собственные <s>вектора </s> операторы и сенсоры; самодельные внешние пакеты

#### Challenge

1. Сделать DAG из трёх шагов, использующий telegram bot API.
1. Бот публикует сообщение в групповой чат с кнопкой "Поехали" под сообщением.
   Вас добавят в группу. Токен будет в чате.
1. Сенсор в пайплайне ждёт когда кто-то нажмёт на кнопку под сообщением в телеге.
   Группа и бот общий для всех, так что не стесняйтесь помогать
   тестировать друг другу.
1. Распарсите **нужный** апдейт от бота. Сохраните метаданные
   в таблицу в airtable.
   [Документация по доступам](img/w3-airtable-access.png)
   (картинка, 4 Mb).
1. Вы можете сделать DAG без расписания и триггерить его руками из админки.

Технические (и не очень) тонкости:

- Бот, токен и группа где этот бот есть &mdash; получить у оргов;
- Можно использовать какую-то библиотеку но в целом здесь
  хватит грамотного использования `requests`, так как вам
  не требуется сложного взаимодействия с пользователем.
  [Заготовка такого класса для бота](snippets/w3-example-tg-bot-class.py);
- Для сохранения какой-то промежуточной информации используйте временный файл на диске;
- Для тестирования можно создать свою airtable базу/таблицу;
- Бот и группа общие для всех. Создавать отдельного бота чтобы отладить как это работает мы не рекомендуем:
  возможные незначительные технические трудности с доступами могут надолго отвлечь от задачи;
- Финальный датасет содержит следующие колонки:
  `chat_id`,
  `username`,
  `triggered_at`,
  `event_type`,
  `reporter_name`.
  Их типы можно подсмотреть прямо в таблице;
- Подразумевается, что вы будете использовать самодельные операторы/сенсоры и опубликуете их как библиотеку на github;
- В данном задании можно захардкодить токен для доступа прям в коде вашего пайплайна.
  Если вы решите так сделать, то не выкладывайте код в публичный репозиторий.

#### Материалы для изучения

Дополнительные ссылки на почитать к сегодняшнему вебинару:

- [API ботов телеграм](https://core.telegram.org/bots/api) (вероятно, потребуется VPN).
  Основное, что вам понадобится в этом задании это метод [sendMessage](https://core.telegram.org/bots/api#sendmessage)
  и документация по [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup)
- [Документация по кастомным операторам](https://airflow.apache.org/docs/stable/howto/custom-operator.html)
- [Код Slack-оператора из airflow](https://github.com/apache/airflow/blob/master/airflow/providers/slack/operators/slack.py)
  &mdash; если у вас получается что-то _сложнее_, вы скорее всего делаете что-то не так
- [Пример пайплайна с кастомным оператором](https://technofob.com/2019/05/30/get-started-developing-workflows-with-apache-airflow/).
  Кстати, эта статья вам должна уже казаться достаточно понятной в тех местах где описываются
  базовые вещи как развернуть стенд с airflow
- [Доклад о пакетах в python](https://www.youtube.com/watch?v=yLyW3s1vvUI&list=PLRdS-n5seLRrFxA3PDP0JRz7wRLGJ-xu0&index=14)

### 4. Ветвление и общение DAG между собой

#### Challenge

В этом задании мы апгрейдим то, что получилось во второй домашке.

1. В начало пайпа добавляем оператор, который проверяет, что PostgreSQL для хранения результата доступна.
1. В случае если все ок – едем дальше по пайпу, если нет – скипаем все дальнейшие шаги.
1. Добавляем sanity-check оператор, который проверяет, что данные в порядке и их можно класть в хранилище.
1. В случае если все ок с данными – кладем в PostgreSQL, если нет – шлем уведомление в наш любимый
   чат в Телеге о том, что все плохо.

Требования к DAG:

- "доступность" PostgreSQL довольно растяжимое понятие – решайте сами, что вы в него вкладываете, только напишите об этом;
- при алертах в телегу нужно также передавать task_id и dag_id, но брать их из контекста, а не ручками;
- _очевидно_, что операторы, которые выполняют проверку условий в данном задании должны быть экземплярами наследников
  класса BaseBranchOperator.

#### Материалы для изучения

Дополнительные ссылки на почитать к сегодняшнему вебинару:

- [Исходники `BaseBranchOperator`](https://airflow.apache.org/docs/stable/_api/airflow/operators/branch_operator/index.html?highlight=branch#module-airflow.operators.branch_operator)
- [Гайд по обмену данными в Airflow](https://www.astronomer.io/guides/airflow-datastores/)
- [Где посмотреть execution context](https://bcb.github.io/airflow/execute-context)

## Contributing

Хотя это материалы конкретного курса, мы будем рады, если вы захотите добавить
материала по темам курса, дать ссылки на более актуальные статьи или полезные
инструменты, которые мы не рассмотрели. Если вы поправите ошибку или неточность –
мы тоже будем рады.
