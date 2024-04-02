from flask import Flask, render_template
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


@app.route("/toppage/")
def toppage():
    return render_template('toppage.html')


if __name__ == "__main__":
    app.run(debug=True)
