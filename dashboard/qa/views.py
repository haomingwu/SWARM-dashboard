from flask import Blueprint, render_template, current_app, jsonify, request, redirect, url_for
from ..user import User
from flask_login import current_user
from ..dbs import db
from .models import Question,Answer,Comment

qa = Blueprint('qa', __name__, url_prefix='')


@qa.route('/', methods=["GET"])
def index():
    return render_template("qa/index.html", current_user=current_user)

@qa.route('/question/add', methods=["GET"])
def add_question():
        return render_template("qa/ask_question.html")

@qa.route('/question', methods=["GET", "POST"])
def question_info():
    try:
        if request.method == "POST":
            if not current_user.is_authenticated:
                return jsonify(status="error", info=u"Please Login Firstly")
            question_instance = Question.query.filter(Question.name==request.form['title']).first()
            if question_instance:
                return jsonify(status="error", info=u"Question Exists")
            else:
                question_instance = Question()
                question_instance.author_id = current_user.id
                question_instance.name = request.form['title']
                question_instance.content = request.form['content']
                db.session.add(question_instance)
                db.session.commit()
                return jsonify(status="success", info=u"Successfully Post")
        else:
            question_list = Question.query.filter().all()
            return render_template("qa/questions.html", qss=question_list)
    except Exception as e:
        current_app.logger.error(e)
        if request.method == "POST":
            return jsonify(status="error", info=u"Error")
        else:
            return redirect(url_for('qa.index'))


@qa.route('/question/<int:question_id>', methods=['GET', 'POST'])
def questions(question_id):
    try:
        if request.method == "GET":
            question_instance = Question.query.filter(Question.id==question_id).first()
            if question_instance:
                return render_template("qa/question_detail.html", qs=question_instance)
            return redirect(url_for('qa.index'))
    except Exception as e:
        current_app.logger.error(e)
        return redirect(url_for('qa.index'))

                 


@qa.route('/question/<int:question_id>/answer', methods=['POST'])
def add_answer(question_id):
    try:
        if not current_user.is_authenticated:
            return jsonify(status="error", info=u"Please Login Firstly")
        question_instance = Question.query.filter(Question.id==question_id).first()
        if not question_instance:
            return jsonify(status="error", info=u"No such question")
        else:
            if request.form['rtype'] == "1":
                answer_instance = Answer()
                answer_instance.content = request.form['content']
                answer_instance.author_id = current_user.id
                answer_instance.question_id = question_id
                question_instance.answers_count += 1
                db.session.add(question_instance)
                db.session.add(answer_instance)
            elif request.form['rtype'] == "2":
                answer_instance = Answer.query.filter(Answer.id==request.form['rid']).first()
                if not answer_instance:
                    return jsonify(status="error", info=u"Error")
                comment_instance = Comment()
                comment_instance.content = request.form['content']
                comment_instance.author_id = current_user.id
                comment_instance.answer_id = answer_instance.id
                answer_instance.comments_count += 1
                db.session.add(answer_instance)
                db.session.add(comment_instance)
            else:
                return jsonify(status="error", info=u"Error")

            db.session.commit()
            return jsonify(status="success", info=u"Successfully Replied")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(status="error", info=u"Error")


