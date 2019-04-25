from flask import Flask, redirect, url_for, render_template, jsonify, request, flash, make_response
from flask_login import login_required, current_user
import datetime
import click

from Model import *
from ext.login_manger import loginmanager

from bp import auth, room, notification, admin

app = Flask(__name__)
app.register_blueprint(auth.authbp)
app.register_blueprint(room.roombp)
app.register_blueprint(notification.notificationbp)
app.register_blueprint(admin.adminbp)

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


@app.before_first_request
def beforefirstreq():
    # 添加管理员角色
    adminrole = Role.query.filter_by(role_name="admin").first()
    if (adminrole == None):
        newadminrole = Role(role_name="admin", need_actice=True)
        db.session.add(newadminrole)
        db.session.commit()


# db.drop_all(app=app)
# db.create_all(app=app)


@app.cli.command()
@click.option("--drop", is_flag=True, help="drop all database")
def dropdb(drop):
    if(drop):
        db.drop_all()

@app.cli.command()
@click.option("--create", is_flag=True, help="create all database")
def dropdb(drop):
    if(drop):
        db.create_all()

@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')

# @app.errorhandler(500)



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
