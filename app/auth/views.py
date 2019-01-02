from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import User
from .forms import LoginForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('邮箱或者密码错误!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', "POST"])
def logout():
    logout_user()
    flash('成功退出!')
    return redirect(url_for("main.index"))
