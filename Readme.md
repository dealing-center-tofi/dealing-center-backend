Dealing center
--------------

<br>

# How to clone, install and use
## Install pre-requisites

###Virtualenv
Standard installation with <b>virtualevnwrapper</b>.

###PostgreSQL
Standard installation.

<br>

## Standard project initialization
### 1. Create virtual environment

1. Clone repository: ``git clone https://github.com/dealing-center-tofi/dealing-center-backend``
2. Create virtual environment: ``mkvirtualenv dealing-center``
3. Install requirements ``pip install -r requirements.txt``
4. Edit $VIRTUAL_ENV/bin/postactivate to contain the following lines:


    export DATABASE_URL=YOUR_DATABASE_URL (like ``postgresql://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME``)
    export ENV=dev


5. Deactivate and re-activate virtualenv:

```
deactivate
workon dealing-center
```

<br>

### 2. Database

1. Create database table:


    psql -Uyour_psql_user
    CREATE DATABASE YOUR_DB_NAME(dealing_center, for example)


2. Migrations: ``./manage.py migrate``
3. Create admin: ``./manage.py createsuperuser``

<br>

### 3. Run the server 

    ./manage.py runserver
