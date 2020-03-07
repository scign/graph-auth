class Config(object):
    TESTING = False
    DEVELOPMENT = False
    DEBUG = False


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