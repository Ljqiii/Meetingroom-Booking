from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, current_user
import calendar
import datetime
from Form import Register, Role, Login
from Model import User, db, Room

roombp = Blueprint("room", __name__, static_folder='static', static_url_path="/static",
                   template_folder="/templates/room/")


@roombp.route("/state")
def roomstate():
    roomlist = list(Room.query.all())
    return render_template("room/state.html", roomname="room", roomlist=roomlist)


@roombp.route("/room/<string:roomname>")
def roomstatus(roomname):
    roomlist = list(Room.query.all())

    model = {}
    model["date"] = []
    model["roomlist"] = roomlist
    model["roomname"] = roomname

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    today=datetime.datetime(year,month,day)
    aweekin=today+datetime.timedelta(days=7)



    weekday, lastday = calendar.monthrange(year, month)
    weekday = weekday + 1 #星期几

    for i in range(7):
        model["date"].append(today+datetime.timedelta(days=i))

    for i in roomlist:
        if (roomname == i.roomname):
            return render_template("room/state.html", model=model)
        else:
            return render_template("error.html", errmsg="未找到此教室")
