====================
Flask-Simon Examples
====================

Here are some exaples of using Flask-Simon


Flaskr
======

Flaskr_ is the tutorial that ships with Flask. It uses SQLite as its
database. The ``flaskr`` folder contains the Flaskr code modified to
use Flask-Simon.

The biggest change is all of the database setup work has been removed
as Flask-Simon and MongoDB will take care of it for you.

.. _Flaskr: http://flask.pocoo.org/docs/tutorial/


Flask-Login
===========

`Flask-Login`_ is a popular library for handling a user's session. An
example of using it with Flask-Simon can be found in the ``flask-login``
folder.

Keep in mind that this is only an example. The ``login`` view checks for
the password stored as plain text. When implementing your own login,
make sure to hash your passwords using an algorithm such as PBKDF2_.

.. _Flask-Login: http://packages.python.org/Flask-Login/
.. _PBKDF2: http://en.wikipedia.org/wiki/PBKDF2
