# - coding: utf-8 --

class Config(object):
    CORS_HEADERS = 'Content-Type'
    SECRET_KEY = 'ASSdsWFG5GljejfewjfopjeofopefjepfjpefoejfE65R8EG4H4TRRS6FG46S4G8RG6S'
    BUNDLE_ERRORS = True
    RESTX_VALIDATE = True
    ERROR_404_HELP = False
    RESTX_MASK_SWAGGER = False


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


config_dict = {
    'Production': ProductionConfig,
    'Development': DevelopmentConfig,
    'Debug': DebugConfig
}
