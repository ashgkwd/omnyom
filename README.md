# OmNyom Feed Reader

## Setup

To get the application running:

```bash
# build the main app image
docker compose build omnyom

# set up the database
docker compose up -d pg
export POSTGRES_USER=devuser
docker compose exec pg psql -U $POSTGRES_USER -c "create database omnyom owner $POSTGRES_USER;"
docker compose exec pg psql -U $POSTGRES_USER -c "create database test_omnyom owner $POSTGRES_USER;"
docker compose run omnyom "flask db upgrade"

# start containers and tail logs
docker compose up -d
docker compose logs -f
```

To get in a running container:

```bash
docker compose exec omnyom bash
```

## Running tests

To run tests in a running container:

```bash
docker compose exec omnyom env APP_SETTINGS="app.config.TestConfig" pytest
```

To run tests on a clean test db:

```bash
bin/runtests
```

## Development

If you want to run any flask command, run it through the docker container

```bash
docker compose run omnyom 'flask do the magic'
# docker compose run omnyom 'flask db migrate'
```

## Schema

Feed

- has_many: Feed Items
- url
- created_by: User
- created_at

Feed Item

- belongs_to: Feed
- external_id (string)
- title
- summary
- author
- published_at
- metadata (json)
- content (text)

User

- email
- name

Subscription

- belongs_to: User
- belongs_to: Feed

Feed Item Read

- belongs_to: Feed Item
- belongs_to: Subscription
- is_read (bool)
