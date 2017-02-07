import os

# Flask config
DEBUG=False
IP=os.environ.get('SUPERLATIVES_IP', '0.0.0.0')
PORT=os.environ.get('SUPERLATIVES_PORT', 8080)
SERVER_NAME = os.environ.get('SUPERLATIVES_SERVER_NAME', 'superlatives.csh.rit.edu')
SECRET_KEY = os.environ.get('SUPERLATIVES_SECRET_KEY', '')

# OpenID Connect SSO config
OIDC_ISSUER = os.environ.get('SUPERLATIVES_OIDC_ISSUER', 'https://sso.csh.rit.edu/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': os.environ.get('SUPERLATIVES_OIDC_CLIENT_ID', 'superlatives'),
    'client_secret': os.environ.get('SUPERLATIVES_OIDC_CLIENT_SECRET', ''),
    'post_logout_redirect_uris': [os.environ.get('SUPERLATIVES_OIDC_LOGOUT_REDIRECT_URI',
                                                 'https://superlatives.csh.rit.edu/logout')]
}

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SUPERLATIVES_DATABASE_URI',
    'sqlite:///{}'.format(os.path.join(os.getcwd(), 'data.db')))
