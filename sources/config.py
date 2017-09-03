import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 't_ifJk2jhR,jl$0'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    QUESTION_ARCHIVE_DIR = 'question_archives'
    MP3_DIR = './app/static/mp3'
    ZIP_DIR = './app/static/zip'
    MESSAGES_ARCHIVE_FILENAME = 'messages.txt'
    UPDATE_STATUS = False
    CLIENT_STACK = []
    CLIENT_NUMBER = 1
    QUESTION_ACTIVE = 1
    
    CREDENTIALS = [
                {'loginUser':'EVAL_5349668',
                'loginPassword':'94wbhtnb'}
                ]
    CREDENTIAL_NUM = 0



#class ProductionConfig(Config):
#    DEBUG = False
#
#
#class StagingConfig(Config):
#    DEVELOPMENT = True
#    DEBUG = True
#
#
#class DevelopmentConfig(Config):
#    DEVELOPMENT = True
#    DEBUG = True
#
#
#class TestingConfig(Config):
#    TESTING = True
