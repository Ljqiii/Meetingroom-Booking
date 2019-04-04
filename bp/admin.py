from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import login_user, login_required, current_user, logout_user

from Form import Register, Role, Login
from Model import User, db

adminbp = Blueprint("admin", __name__, static_folder='static', static_url_path="/static", template_folder="/templates/admin/",url_prefix="/admin")


@adminbp.before_request
def verificationadmin():
    if(current_user.username!="admin" or current_user.role.role_name!="admin"):
        return redirect(url_for("auth.nopermission"))
        return current_user.username+current_user.role.role_name

@adminbp.route("/")
@login_required
def admin():
    return render_template("admin/adminindex.html")


@adminbp.route("/roommanage")
@login_required
def roommanage():
    return render_template("admin/roommanage.html")



