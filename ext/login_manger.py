from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from Model import User
loginmanager=LoginManager()


@loginmanager.unauthorized_handler
def unauthorized():
    # a = request
    # host_url = request.host_url
    # full_path = request.full_path
    # ua = request.headers["User-Agent"]
    # referer = request.headers["Referer"]

    return "unauthorized"


@loginmanager.user_loader
def load_user(user_id):
    print(user_id)
    try:
        user_id = int(user_id)
    except:
        user_id = None
    return User.query.filter_by(id=user_id).first()
