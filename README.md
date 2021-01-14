# yiana.backend
Backend for Yiana project

## How to start

1. Ensure you have python 3.9.

2. Check that you have packages listed in requirements/compiled.txt installed in your system or install them manually.

3. Create virtualenv and activate it:

       $ python -m venv yiana.backend
       $ source yiana.backend/bin/activate

4. Install project dependencies::

        $ bin/pip install -r requirements/dev.txt

5. For development, setup development database server (see below)

6. REWRITE FOR ENV - Copy conf/settings_local.py.template to conf/settings_local.py and edit it to suit your environment.

7. To run development server on localhost:

    $ python manage.py runserver 0.0.0.0:8000

8. To run tests:

    $ pytest


## Setup development database server

PostgreSQL version 12.5, should be used as development database
server. The PostgreSQL user should be able to create and drop databases in default schema, in order Django could run automated tests.

For installing, follow the steps:

1. Install PostgreSQL on your working machine
   (see requirements/compiled.txt)
2. Run PostgreSQL console and perform following actions:
        * Create user named 'yiana_admin'
        * Grant permissions to create databases and tables on default tablespace.
   For this, run the commands:

    $ sudo -u postgres psql

    postgres=# CREATE USER yiana_admin WITH PASSWORD 'yianasecret';
    CREATE ROLE
    postgres=# GRANT CREATE on TABLESPACE pg_default TO yiana_admin;
    GRANT
    postgres=# ALTER USER yiana_admin CREATEDB;
    ALTER ROLE
    postgres=# \db+
			   List of tablespaces
      Name    |  Owner   | Location |  Access privileges     | Description
    ------------+----------+----------+------------------------+-------------
    pg_default | postgres |          | postgres=C/postgres+   |
	       |          |          | yiana_admin=C/postgres |
    pg_global  | postgres |          |                        |
    (2 rows)

    postgres=# \q

3. Add user permissions to **pg_hba.conf**:
    local   all    yiana_admin   trust

4. Restart postgres::

        $ sudo systemctl restart postgresql.service

5. Create development database::

        $ createdb -U yiana_admin -D pg_default yiana


How to deploy
-------------

1. Install everything, listed in the sections above;

2. Create supervisor configuration from template::

    $ cp supervisord.conf.sample supervisord.conf

3. Setup reverse HTTP proxy (nginx, whatever);

4. Edit supervisor configuration according on current environment;

5. Update and restart all in supervisor::

    $ bin/supervisorctl restart all
    gunicorn: stopped
    gunicorn: started