# Project for referrals registration

This REST API is made for [test](https://docs.google.com/document/d/1YaiDiza5U3i0ZxmYuZt7ZCRgGycLgDnq/edit) project
<br/>

## Running on:

* Windows 11

* Python 3.11.4 or higher

* PostgreSQL
* Redis

## How to run

### Install from git:

```shell
$ git clone https://gitflic.ru/project/abstract-333/referral-api.git
```

### Install dependencies:

```shell
$ pip install -r requirements.txt
```

### Make migration for database:

_<strong>
First Create database under "name".
<br>
Add this name and other properties to .env.prod file.
</strong>_
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

## Main Concepts:

* Using [Refresh and Access Tokens](https://stateful.com/blog/oauth-refresh-token-best-practices), so we don't have to
  ask
  user every time for credentials in order to make authorization complete, also it makes our app safer even if someone
  else stole user's access token it will be valid for short period. When user needs new access token he can use his
  refresh
  token in order to get new access and refresh tokens, and old refresh token will be sent to blacklist. Sign-out do the
  same almost but here we don't return any tokens to user obviously :).
* [Dynamic Salt](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/) is a great choice when
  you need to secure your password hash from rainbow table.
* Implementing UoW and repository patterns.
* [UUID v7](https://www.ietf.org/archive/id/draft-peabody-dispatch-new-uuid-format-04.html#name-uuid-version-7) is must
  have.
* Adding Docs for all routers.
* Using pydantic in order to make validation simple and safe,
  also [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) sounds good to store
  environment
  variables in one place.
* For referral code I use [Nano ID](https://zelark.github.io/nano-id-cc/).
* Using [Brotli Compression](https://www.coralnodes.com/gzip-vs-brotli/)
  and [ORJSON](https://github.com/ijl/orjson), which increase the
  performance of this api.
  ![ORJSON](https://github.com/ijl/orjson/raw/master/doc/serialization.png)

## ERD:

![referral_db](./images/referral_db.jpg)