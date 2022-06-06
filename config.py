from distutils.debug import DEBUG


class DevelopmentConfig():
    DEBUG = True

class ProductionConfig():
    DEBUG = False 

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}