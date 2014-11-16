import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = os.path.join(basedir, 'uploads_images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
WHOOSH_BASE = os.path.join(basedir, 'search.db')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'asdfaASKDF87#$#ASMASDFJSN88skdnfas!@@@mksJSK'
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

