============================================
Flask-Simon: Simple MongoDB Models for Flask
============================================

.. image:: https://secure.travis-ci.org/dirn/Flask-Simon.png?branch=develop
   :target: http://travis-ci.org/dirn/Flask-Simon


Getting Started
===============

Connect to the database::

    from flask import Flask
    from flask.ext.simon import Simon

    app = Flask(__name__)
    Simon(app)

Full documentation can be found on `Read the Docs`_.

.. _Read the Docs: http://flask-simon.readthedocs.org


Installation
============

Installing Flask-Simon is easy::

    pip install Flask-Simon

or download the source and run::

    python setup.py install
