import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = os.path.join(basedir, 'uploads_images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

WTF_CSRF_ENABLED = True
SECRET_KEY = 'asdfaASKDF87#$#ASMASDFJSN88skdnfas!@@@mksJSK'