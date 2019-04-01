from flask import Flask, redirect, url_for, render_template, jsonify, request, flash, make_response
from flask_login import login_required, current_user
import datetime

from Model import *
from ext.login_manger import loginmanager

from bp import auth, room, notification

app = Flask(__name__)
app.register_blueprint(auth.authbp)
app.register_blueprint(room.roombp)
app.register_blueprint(notification.notificationbp)

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

loginmanager.init_app(app)
db.init_app(app)


# db.drop_all(app=app)
# db.create_all(app=app)

# role1 = Role(id="1", role_name="11", need_actice=True)
# role2 = Role(id="2", role_name="22", need_actice=True)

# db.session.add(role1)
# db.session.add(role2)
# db.session.commit()


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
    return render_template("index.html")


@app.route("/book")
def booking():
    return "booking"


@app.route("/cancel")
def cancel():
    return "cancel"


@app.route("/allrole")
def allrole():
    b = Role.query.all()
    allrolelist = {str(i.id): str(i.need_actice) for i in Role.query.all()}
    b = 1


if __name__ == '__main__':
    app.run()
