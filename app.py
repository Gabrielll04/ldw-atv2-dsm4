from flask import Flask, render_template
from controllers import routes
from models.database import db
import pymysql

app = Flask(__name__, template_folder='views')
routes.init_app(app)

DB_NAME = 'pokemon'
app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root@localhost/{DB_NAME}'

app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Iniciar o servidor
if __name__ == '__main__':
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print("O banco de dados foi criado!")
    except Exception as e:
        print(f"Erro ao criar o banco: {e}")
    finally:
        connection.close()

    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=4000, debug=True)
