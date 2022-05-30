import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_LEVEL                           = os.environ.get('LOG_LEVEL', 'WARNING').upper()
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')
    BASIC_USER                          = os.getenv('BASIC_USER')
    BASIC_PASSWORD                      = os.getenv('BASIC_PASSWORD')


