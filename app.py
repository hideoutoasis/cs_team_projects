from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class notice(db.Model):
    noticeID = db.Column(db.Integer, primary_key=True)
    noticeTitle = db.Column(db.String(100), nullable=False)
    noticeContents = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.noticeTitle} {self.noticeContents}'
    # 게시판 DB테이블 설계부분입니다.

with app.app_context():
    db.create_all()

@app.route("/")
def toppage():
    notice_list = notice.query.all()
    return render_template('toppage.html', data=notice_list)

@app.route("/toppage/create/")
def post_create():
    title_receieve = request.args.get("noticeTitle")
    content_receieve = request.args.get("noticeContents")
    # form에서 보낸 데이터 받아오는 부분입니다.

    noticetable = notice(noticeTitle=title_receieve, noticeContents=content_receieve)
    db.session.add(noticetable)
    db.session.commit()
    return redirect(url_for('toppage', noticeTitle=title_receieve))
    # DB에 저장되도록 연결해주는 부분입니다.
    # 위에서부터 DB와 연결하여 데이터를 보내고, 테이블을 추가하고, 커밋하여 저장하는 기능을 합니다.
    # 커밋 코드는 html에서 데이터를 받아 반환해 주는(?) 기능을 합니다.
    # 마지막 코드는 자동 리다이렉트로 작성한 게시글이 바로바로 반영되게 만들어 줍니다.
    
@app.route('/toppage/delete/<int:noticeID>')
# noticeID 가 Null일 경우 처리
# @app.route('/delete', defaults={'noticeID': None})
def delete(noticeID):
    notice_delete = notice.query.filter_by(noticeID=int(noticeID)).first()

    db.session.delete(notice_delete)
    db.session.commit()

    return redirect(url_for('toppage'))

if __name__ == "__main__":
    app.run(debug=True)
