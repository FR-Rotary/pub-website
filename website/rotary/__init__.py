import os

from flask import Flask, redirect, url_for
from flask_compress import Compress
from flask_talisman import Talisman

# A CSP copied from the talisman documentation and added code until the website wasn't broken anymore. Could probably be improved.
CSP_POLICY = {
    # <iframe> based embedding for Maps.
    'frame-src': '\'self\' www.google.com',
    'script-src': '\'self\' \'nonce-{nonce}\' code.jquery.com cdn.datatables.net',
    'style-src': '\'self\' \'nonce-{nonce}\' \'unsafe-inline\' cdn.datatables.net',
}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Compress(app) #Compress responses, a fast website is a good website
    Talisman(app, content_security_policy=CSP_POLICY, content_security_policy_nonce_in=['script-src']) #Extension that sets security headers

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('ROTARY_SECRET_KEY', 'dev'),
        DATABASE=os.environ.get(
            'ROTARY_DATABASE',
            os.path.join(app.instance_path, 'rotary.sqlite')
        ),
        USERNAME=os.environ.get('ROTARY_USERNAME', 'dev'),
        PASSWORD=os.environ.get('ROTARY_PASSWORD', 'password'),
        SMTP_HOST=os.environ.get('ROTARY_SMTP_HOST'),
        SMTP_PORT=os.environ.get('ROTARY_SMTP_PORT', 587),
        SMTP_USERNAME=os.environ.get('ROTARY_SMTP_USERNAME'),
        SMTP_PASSWORD=os.environ.get('ROTARY_SMTP_PASSWORD'),
        CONTACT_FORM_ADDRESS=os.environ.get('ROTARY_CONTACT_FORM_ADDRESS'),
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

    @app.route('/internt/')
    def internt_slash_redirect():
        return redirect(url_for('internal.index'))

    @app.route('/internt')
    def internt_redirect():
        return redirect(url_for('internal.index'))

    from . import countries
    app.jinja_env.globals.update(
        to_letter_code=countries.to_letter_code,
        to_pretty_name=countries.to_pretty_name
    )

    from . import util
    app.jinja_env.globals.update(
        format_time=util.format_time
    )

    from . import mail

    return app

app = create_app()
