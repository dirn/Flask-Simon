====================
Flask-Simon Examples
====================

Here are some exaples of using Flask-Simon

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
