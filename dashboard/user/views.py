from flask import (Blueprint, request, current_app, redirect, url_for,
        jsonify)
from .models import User
from sqlalchemy import or_
from ..dbs import db
from flask_login import login_user, logout_user, login_required


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/signup', methods=['POST'])
def signup_user():
    try:
        user_instance = User.query.filter(or_(User.name==request.form['name'],
                                            User.email==request.form['email'])).first()
        if user_instance:
            return jsonify(status="error", info=u"User Exists")
        else:
            user_instance = User()
            user_instance.name = request.form['name']
            user_instance.email = request.form['email']
            user_instance.set_password(request.form['password'])
            db.session.add(user_instance)
            db.session.commit()
            return jsonify(status="success", info=u"Successfully Registered")
    except Exception as e:
        current_app.logger.error(e)
        return redirect(url_for('qa.index'))


@user.route('/login', methods=['POST'])
def login_users():
    print('in login')
    try:
        user_instance = User.query.filter(User.name==request.form['name']).first()
        print(user_instance)
        if user_instance:
            if user_instance.verify_password(request.form['password']):
                print('login ok')
                login_user(user_instance)
        return redirect(url_for('qa.index'))
    except Exception as e:
        current_app.logger.error(e)
        return redirect(url_for('qa.index'))


@user.route('/logout', methods=['GET'])
@login_required
def logout_users():
    logout_user()
    return redirect(url_for('qa.index'))
