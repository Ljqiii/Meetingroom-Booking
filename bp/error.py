from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import login_user, login_required, current_user, logout_user

from Form import Register, Role, Login
from Model import User, db

errorbp = Blueprint("error", __name__, static_folder='static', static_url_path="/static", template_folder="templates")

@errorbp.route("/error", methods=["GET"])
def errpage():
    return render_template("error.html",errmsg="err")
