#: The title of this site
SITE_TITLE = 'Wiktionary'
#: TypeKit code for fonts
TYPEKIT_CODE = ''
#: Secret key
SECRET_KEY = 'make this something random'
#: PORT_NO
PORT_NO = 3333
#: ENVIRONMENT should be dev
ENVIRONMENT = u'gevent'
#: IP to run
IP = '0.0.0.0'
#: Mediawiki settings
MEDIAWIKI = {
    'host': 'http://78.46.204.24',
    'api': '/api.php'
    }
#: Database backend
SQLALCHEMY_DATABASE_URI = 'postgres://aadukalam:postgres-aadukalam@78.46.204.24:5432/wikimedia'
#: Full path of project directory + wiktionary.json file
SAMPLE_FILE_PATH = "/home/kracekumar/Dropbox/codes/python/python/flask/sandbox/wikimedia/python-wiktionary/wiktionary.json"
