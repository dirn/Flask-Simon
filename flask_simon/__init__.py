from flask import abort
from pymongo import uri_parser
import simon.connection

__all__ = ('Simon', 'get_or_404')


class Simon(object):
    """Automatically creates a default connection for Simon models."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the Flask app for use with Simon.

        This method will automatically be called if the app is passed
        into ``__init__()``.

        :param app: the Flask application.
        :type app: :class:`flask.Flask`
        """

        if 'simon' not in app.extensions:
            app.extensions['simon'] = {}

        if 'MONGO_URI' in app.config:
            parsed = uri_parser.parse_uri(app.config['MONGO_URI'])
            if not parsed.get('database'):
                raise ValueError('MONGO_URI does not contain a database name.')

            app.config['MONGO_DBNAME'] = parsed['database']
            app.config['MONGO_USERNAME'] = parsed['username']
            app.config['MONGO_PASSWORD'] = parsed['password']
            app.config['REPLICA_SET'] = parsed['options'].get('replica_set')

            host = app.config['MONGO_URI']
            name = app.config['MONGO_DBNAME']
            username = app.config['MONGO_USERNAME']
            password = app.config['MONGO_PASSWORD']
            replica_set = app.config['REPLICA_SET']

            simon.connection.connect(host_or_uri=host, name=name,
                                     username=username, password=password,
                                     replica_set=replica_set)
        else:
            host = app.config['HOST'] = 'localhost'
            name = app.config['MONGO_DBNAME'] = app.name

            simon.connection.connect(host=host, name=name)


def get_or_404(model, *qs, **fields):
    """Finds and returns a single document, or raises a 404 exception.

    This method will find a single document within the specified
    model. If the specified query matches zero or multiple documents,
    a ``404 Not Found`` exception will be raised.

    :param model: the model class.
    :type model: :class:`simon.Model`
    :param \*qs: logical queries.
    :type \*qs: :class:`simon.query.Q`
    :param \*\*fields: keyword arguments specifying the query.
    :type \*\*fields: kwargs

    .. versionadded: 0.1.0
    """

    try:
        return model.get(*qs, **fields)
    except (model.NoDocumentFound, model.MultipleDocumentsFound):
        abort(404)
