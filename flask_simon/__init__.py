__version__ = '0.3.0'

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import abort
from pymongo import uri_parser
from simon import Model, connection, geo, query
from werkzeug.routing import BaseConverter

__all__ = ('Simon', 'get_or_404', 'Model', 'connection', 'geo', 'query')


class ObjectIDConverter(BaseConverter):
    """Convert Object IDs for use in view routing URLs."""

    def to_python(self, value):
        try:
            return ObjectId(value)
        except (InvalidId, TypeError):
            abort(400)

    def to_url(self, value):
        return str(value)


class Simon(object):
    """Automatically creates a connection for Simon models."""

    def __init__(self, app=None, prefix='MONGO', alias=None):
        if app is not None:
            self.init_app(app, prefix, alias)

    def init_app(self, app, prefix='MONGO', alias=None):
        """Initializes the Flask app for use with Simon.

        This method will automatically be called if the app is passed
        into ``__init__()``.

        :param app: the Flask application.
        :type app: :class:`flask.Flask`
        :param prefix: (optional) the prefix of the config settings
        :type prefix: str
        :param alias: (optional) the alias to use for the database
                      connection
        :type alias: str

        .. versionchanged:: 0.2.0
           Added support for multiple databases
        .. versionadded:: 0.1.0
        """

        if 'simon' not in app.extensions:
            app.extensions['simon'] = {}

        app.url_map.converters['objectid'] = ObjectIDConverter

        def prefixed(name):
            """Prepends the prefix to the key name."""

            return '{0}_{1}'.format(prefix, name)

        # The URI key is accessed a few times, so be lazy and only
        # generate the prefixed version once.
        uri_key = prefixed('URI')

        if uri_key in app.config:
            parsed = uri_parser.parse_uri(app.config[uri_key])
            if not parsed.get('database'):
                message = '{0} does not contain a database name.'
                message = message.format(uri_key)
                raise ValueError(message)

            host = app.config[uri_key]

            name = app.config[prefixed('DBNAME')] = parsed['database']
            username = app.config[prefixed('USERNAME')] = parsed['username']
            password = app.config[prefixed('PASSWORD')] = parsed['password']

            replica_set = parsed['options'].get('replicaset', None)
            app.config[prefixed('REPLICA_SET')] = replica_set
        else:
            host_key = prefixed('HOST')
            port_key = prefixed('PORT')
            name_key = prefixed('DBNAME')
            username_key = prefixed('USERNAME')
            password_key = prefixed('PASSWORD')
            replica_set_key = prefixed('REPLICA_SET')

            app.config.setdefault(host_key, 'localhost')
            app.config.setdefault(port_key, 27017)
            app.config.setdefault(name_key, app.name)

            app.config.setdefault(username_key, None)
            app.config.setdefault(password_key, None)
            app.config.setdefault(replica_set_key, None)

            host = app.config[host_key]
            port = app.config[port_key]
            name = app.config[name_key]
            username = app.config[username_key]
            password = app.config[password_key]
            replica_set = app.config[replica_set_key]

            host = '{0}:{1}'.format(host, port)

        connection.connect(host, name=name, alias=alias, username=username,
                           password=password, replica_set=replica_set)


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
    :returns: :class:`~simon.Model` -- an instance of a model.

    .. versionadded: 0.1.0
    """

    try:
        return model.get(*qs, **fields)
    except (model.NoDocumentFound, model.MultipleDocumentsFound):
        abort(404)
