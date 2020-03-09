import os

class Config(object):
    TESTING = False
    DEVELOPMENT = False
    DEBUG = False
    AZURE_APP_ID = os.environ.get('AZURE_APP_ID', None)
    AZURE_APP_SECRET = os.environ.get('AZURE_APP_SECRET', None)
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID', 'common')
    if AZURE_APP_ID is None:
        raise EnvironmentError('AZURE_APP_ID is not set')
    if AZURE_APP_SECRET is None:
        raise EnvironmentError('AZURE_APP_SECRET is not set')
    SECRET_KEY = AZURE_APP_SECRET


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True