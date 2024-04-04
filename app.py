from datetime import datetime
from flask import Flask, render_template, url_for, request
import os
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.utils import redirect


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, db.ForeignKey(
        'notice.id', ondelete='CASCADE'))
    notice = db.relationship('Notice', backref=db.backref('answer_set'))
    comment_username = db.Column(db.String, nullable=False)
    comment_contents = db.Column(db.Text(), nullable=False)
    comment_date = db.Column(db.DateTime(), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    posts = Notice.query.all()  # post 모든 쿼리를 가져옴
    # 각 데이터의 필드를 따로 분리하여 리스트에 저장
    ids = [post.id for post in posts]
    usernames = [post.username for post in posts]
    subjects = [post.subject for post in posts]
    contents = [post.content for post in posts]
    create_dates = [post.create_date for post in posts]
    # index.html 템플릿으로 필드 리스트를 전달  앞에 이름은 py에 있는 이름 = 뒤에 이름은 html에서 내가 쓸 이름
    return render_template('index.html', posts=posts, ids=ids, usernames=usernames, subjects=subjects, contents=contents, create_dates=create_dates)


@app.route('/post_add')
def post_add():
    return render_template('post_add.html')


@app.route('/post_add_button', methods=['GET', 'POST'])
def post_add_button():
    username_receive = request.args.get("username")
    subject_receive = request.args.get("subject")
    content_receive = request.args.get("content")
    # 현재 시각을 가져오기
    current_datetime = datetime.now()
    # 새로운 게시물 생성
    new_post = Notice(username=username_receive, subject=subject_receive,
                    content=content_receive, create_date=current_datetime)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('home'))


# --------댓글 부분 서버-------------------
@app.route('/comment_add/<int:notice_id>')
def comment_add(notice_id):
    comments = Answer.query.filter(Answer.notice_id==notice_id).all()
    return render_template('post.html',notice_id=notice_id, comments=comments)

# html로 받을 것만 여기다 넣어주면 됨


@app.route('/comment_add_button/<int:notice_id>', methods=['GET', 'POST'])
def comment_add_button(notice_id):
    notice = Notice.query.get(notice_id)
    comment_username_receive = request.args.get("comment_username")
    comment_contents_receive = request.args.get("comment_contents")
    # 현재 시각을 가져오기
    current_datetime = datetime.now()
    # 새로운 댓글 생성
    new_answer = Answer(comment_username=comment_username_receive, notice = notice,
                        comment_contents=comment_contents_receive, comment_date=current_datetime)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('comment_add', notice_id=notice_id))


if __name__ == "__main__":
    app.run(debug=True)
