from __future__ import print_function
from __future__ import unicode_literals

from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

from auth import configure_auth
from cache import configure_cache
from mongo import configure_mongo
from pubsub import configure_kafka
from apis import load_apis
from models import load_models


# configure query app
def configure_app(app, config):
    CORS(app) # cross domain

    tools = {
        'auth': configure_auth(app, config),
        'cache': configure_cache(app, config)
    }

    if config.getboolean('hippo', 'mongo'):
        tools['mongo'] = configure_mongo(config)

    if config.getboolean('hippo', 'kafka'):
        tools['pubsub'] = configure_kafka(config)

    models = load_models(tools)
    apis = load_apis(config, tools, models)

    return tools, apis
