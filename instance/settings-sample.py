#: The title of this site
SITE_TITLE = 'Wiktionary'
#: TypeKit code for fonts
TYPEKIT_CODE = ''
#: Secret key
SECRET_KEY = 'make this something random'
#: PORT_NO
PORT_NO = 3333
#: ENVIRONMENT should be dev
ENVIRONMENT = u'dev'
#: IP to run
IP = '0.0.0.0'
#: Mediawiki settings
MEDIAWIKI = {
    'host': 'http://localhost/mediawiki-1.20.0',
    'api': '/api.php'
    }
#: Database backend
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
