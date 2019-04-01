from flask import Flask, redirect, url_for, render_template, jsonify, request, flash, get_flashed_messages, \
    make_response
from Model import *
import datetime
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from bp import auth,room

app = Flask(__name__)
app.register_blueprint(auth.authbp)
app.register_blueprint(room.roombp)

# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql.ljq557@localhost/meetingroombooking'

app.config["SECRET_KEY"] = "super secret key"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# Flask-login settings
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(days=10)
app.config["REMEMBER_COOKIE_REFRESH_EACH_REQUEST"] = True

if (app.config['DEBUG'] == True):
    from flask_debugtoolbar import DebugToolbarExtension

    app.config["SQLALCHEMY_ECHO"] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    toolbar = DebugToolbarExtension(app)


loginmanager = LoginManager(app)

db.init_app(app)

# db.drop_all(app=app)
# db.create_all(app=app)

# role1 = Role(id="1", role_name="11", need_actice=True)
# role2 = Role(id="2", role_name="22", need_actice=True)

# db.session.add(role1)
# db.session.add(role2)
# db.session.commit()


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

@app.route("/avatar/<string:user_id>")
def getAvatar(user_id):
    return "touxiang"


@app.route("/it")
def insertcurrenttime():
    now = datetime.datetime.now()

    db.session.commit()
    return "ok"


@app.route("/proteced")
@login_required
def testproteced():
    return "proteced" + str(current_user)


@app.route("/")
def index():
    flash("aa","danger")
    return render_template("index.html")

@app.route("/book")
def booking():
    return "booking"


@app.route("/cancel")
def cancel():
    return "cancel"


@app.route("/logout")
def logout():
    logout_user()
    return "logout"


@app.route("/allrole")
def allrole():
    b = Role.query.all()
    allrolelist = {str(i.id): str(i.need_actice) for i in Role.query.all()}
    b = 1


if __name__ == '__main__':
    app.run()
