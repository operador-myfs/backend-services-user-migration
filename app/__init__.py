"""Flask app creation."""

from flask import Flask

from app.user_migration.controller import user_migration
from app.ping import ping

ACTIVE_ENDPOINTS = (("/", ping), ("/api", user_migration))


def create_app():
    """Create Flask app."""
    app = Flask(__name__)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app
