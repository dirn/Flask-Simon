from flask import abort
from pymongo import uri_parser
import simon.connection

__all__ = ('Simon', 'get_or_404')


class Simon(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
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
    try:
        return model.get(*qs, **fields)
    except (model.NoDocumentFound, model.MultipleDocumentsFound):
        abort(404)
