from flask import flash,redirect,url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from Model import User
loginmanager=LoginManager()


@loginmanager.unauthorized_handler
def unauthorized():
    flash("此页面需要登陆","warning")
    return redirect(url_for("auth.login"))


@loginmanager.user_loader
def load_user(user_id):
    print(user_id)
    try:
        user_id = int(user_id)
    except:
        user_id = None
    return User.query.filter_by(id=user_id).first()
