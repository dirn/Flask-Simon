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

===================== ==================================================
``MONGO_URI``         A `MongoDB URI`_ connection string specifying the
                      database connection.
``MONGO_HOST``        The hostname or IP address of the MongoDB server.
                      default: 'localhost'
``MONGO_PORT``        The port of the MongoDB server. default: 27017
``MONGO_DNAME``       The name of the database on ``MONGO_HOST``.
                      Default: ``app.name``
``MONGO_USERNAME``    The username for authentication.
``MONGO_PASSWORD``    The password for authentication.
``MONGO_REPLICA_SET`` The name of the replica set.
===================== ==================================================

.. _MongoDB URI: http://docs.mongodb.org/manual/reference/connection-string/

The ``MONGO_URI`` configuration setting will be used before checking
any other settings. If it's not present, the others will be used.

By default, :class:`~flask_simon.Simon` and
:meth:`~flask_simon.Simon.init_app` will use ``MONGO`` as the prefix for
all configuration settings. This can be overridden by using the
``prefix`` argument.

Specifying a value for ``prefix`` will allow for the use of multiple
databases.

.. code-block:: python

    app = Flask(__name__)

    app.config['MONGO_URI'] = 'mongodb://localhost/mongo'
    app.config['SIMON_URI'] = 'mongodb://localhost/simon'

    Simon(app)
    Simon(app, prefix='SIMON')

This will allow for the use of the ``mongo`` and ``simon`` databases on
``localhost``. ``mongo`` will be available to models through the aliases
``default`` and ``mongo``. ``simon`` will be available through the alias
``simon``. This alias can be changed by using the ``alias`` argument.

.. code-block:: python

    Simon(app, prefix='SIMON', alias='other-database')


Routing
-------

Flask-Simon provides a custom converter to allow for the use of Object
IDs in URLs.

.. code-block:: python

    @app.route('/<objectid:id>')

More information about converters is available in the `Flask API`_.

.. _Flask API: http://flask.pocoo.org/docs/api/#url-route-registrations


API
---

.. automodule:: flask_simon
   :members:

.. autoclass:: flask_simon.ObjectIDConverter

Full details of how to query using :meth:`~flask_simon.get_or_404` can
be found in the :meth:`Simon API <simon.Model.get>`.


Further Reading
---------------

For more information, check out the `Simon docs`_ and the
`MongoDB docs`_.

.. _MongoDB docs: http://www.mongodb.org/display/DOCS/Home
.. _Simon docs: http://simon.readthedocs.org/
