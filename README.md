# nicoplus_blog


## Tech Stack

1. *Flask*

2. *Flak-exts*: Flask-login, Flask-mail, Flaks-Admin, Flask-debugtoolbar, Flask-sqlalchemy, Flask-migrate, Flask-bootstrap3, Flask-uploads, Flask-pagedown

3. *Celery*: Using it to send activation e-mail automatically.

4. *Redis*: As a broker of *Celery* .

5. *Postgresql*: As a main relationsip database.

6. *JS*: To implement some simple button event with ajax.

7. *Vagrant*: *Win8* is host machine and *Ubuntu 16 LTS* is guest machine.

8. *Memcached/Libmc*: I design a cache decorator with Libmc. It can generate key by prefix, name of func and parameters of func; Also, it has *mutex*.
