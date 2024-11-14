class DevelopmentConfig():
    SECRET_KEY = 'FZlXsdyC13'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'ecommerce'

config = {
    'development': DevelopmentConfig
}