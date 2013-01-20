Flask-Simon
===========

Simon_ is a library to help make working with MongoDB easier.
Flask-Simon was created to make it even easier to use Simon_ with your
Flask applications.

.. _Simon: http://simon.readthedocs.org/


Installation
------------

To install the latest stable version of Flask-Simon::

    $ pip install Flask-Simon

or, if you must::

    $ easy_install Flask-Simon

To install the latest development version::

    $ git clone git@github.com:dirn/Flask-Simon.git
    $ cd Flask-Simon
    $ python setup.py install

In addition to Flask-Simon, this will also install:

- Flask (0.8 or later)
- PyMongo (2.1 or later)
- Simon


Quickstart
----------

After installing Flask-Simon, import it where you create your Flask app.

.. code-block:: python

    from flask import Flask
    from flask.ext.simon import Simon

    app = Flask(__name__)
    Simon(app)

:class:`~flask_simon.Simon` will establish a connection to the database
that will be used as the default database for any :class:`~simon.Model`
classes that you define.


Configuration
-------------

:class:`~flask_simon.Simon` looks for the following in your Flask app's
configuration:

============= ==========================================================
``MONGO_URI`` A `MongoDB URI`_ connection string specifying the database
              connection.
============= ==========================================================

If the ``MONGO_URI`` configuration setting is not present,
:class:`~flask_simon.Simon` will connect to ``localhost`` and use a
database named after the Flask app.

.. _MongoDB URI: http://docs.mongodb.org/manual/reference/connection-string/


API
---

.. automodule:: flask_simon
   :members:

Full details of how to use :meth:`~flask_simon.get_or_404` can be found
in the :meth:`Simon API <simon.Model.get>`.


Further Reading
---------------

For more information, check out the `Simon docs`_ and the
`MongoDB docs`_.

.. _MongoDB docs: http://www.mongodb.org/display/DOCS/Home
.. _Simon docs: http://simon.readthedocs.org/
