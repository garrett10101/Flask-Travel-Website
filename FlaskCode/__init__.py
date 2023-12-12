import sys 
sys.dont_write_bytecode = True
from flask import Flask



app = Flask(__name__)

affil_id = 'gad50onewayflighticaocode'
apikey = 'so12lCy6yDiAwVdJHol-O-I5fotLVa5k'

app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypassword'
app.config['MYSQL_DB'] = 'mydatabase'

app.secret_key = 'development key'
app.config['SECRET_KEY']='LongAndRandomSecretKey'

#mail.init_app(app)
from .routes import mail
