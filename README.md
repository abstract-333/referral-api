# Project for referrals registration

This REST API is made for [test](https://docs.google.com/document/d/1YaiDiza5U3i0ZxmYuZt7ZCRgGycLgDnq/edit) project
<br/>

## Main Concepts:

#### Reposository Pattern.

#### Unit of Work Pattern.

## Running on:

* Windows 11

* Python 3.11.4 or higher

* PostgreSQL

## How to run

### Install from git:

```shell
$ git clone https://gitflic.ru/project/abstract-333/quiz-api
```

### Install dependencies:

```shell
$ pip install -r requirements.txt
```

### Make migration for database:

<strong>
First Create dabatabas under "name".
<br>
Add this name and other properties to .env file, so that project could working properly.
</strong>
<br>
<br>

```shell
$ alembic init alembic
$ alembic upgrade head
```

### Run App:

```shell
$ cd src
$ uvicorn app:app --reload
```
