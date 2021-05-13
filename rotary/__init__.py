import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rotary.sqlite'),
        USERNAME='dev',
        PASSWORD='password',
        SMTP_HOST=None,
        SMTP_USERNAME=None,
        SMTP_PASSWORD=None,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import i18n
    app.register_blueprint(i18n.bp)

    from . import external
    app.register_blueprint(external.bp)
    app.add_url_rule('/', endpoint='index')

    from . import internal
    app.register_blueprint(internal.bp)

    from . import countries
    app.jinja_env.globals.update(to_letter_code=countries.to_letter_code, to_pretty_name=countries.to_pretty_name)

    from . import util

    return app
