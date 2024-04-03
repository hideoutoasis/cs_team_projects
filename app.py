from flask import Flask, render_template, redirect, url_for
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


@app.route('/delete/<int:noticeID>')
def delete(noticeID):
    notice = noticeTable.query.get_or_404(noticeID)
    question_id = notice.question.id

    db.session.delete(notice)
    db.session.commit()
    
    return redirect(url_for('question.detail', question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)
