import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'date.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Cote=Cote, Author=Author, Artcle=Artcle)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database.')


class Cote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    # 定义属性关系
    articles = db.relationship('Artcle')

class Artcle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    # 定义外键连接author的id
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)