import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 't_ifJk2jhR,jl$0'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    QUESTION_ARCHIVE_DIR = 'question_archives'
    MP3_DIR = './app/main/static/mp3'
    ZIP_DIR = './app/main/static/zip'
    MESSAGES_ARCHIVE_FILENAME = 'messages.txt'
    
    CREDENTIALS = [
                {'loginUser':'EVAL_5349668',
                'loginPassword':'94wbhtnb'},
                {'loginUser':'EVAL_7269307',
                'loginPassword':'8vewq35k'},
                {'loginUser':'EVAL_7824973',
                'loginPassword':'dbhukc6j'}
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
