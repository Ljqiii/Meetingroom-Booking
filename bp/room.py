from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, current_user

from Form import Register, Role, Login
from Model import User, db

roombp = Blueprint("room", __name__, static_folder='static', static_url_path="/static", template_folder="templates")


@roombp.route("/room/<string:roomname>")
def roomstatus(roomname):


    return str(roomname)



