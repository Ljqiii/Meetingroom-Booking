from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, current_user
import calendar
import datetime
from Form import Register, Role, Login
from Model import User, db, Room, Schedule

roombp = Blueprint("room", __name__, static_folder='static', static_url_path="/static",
                   template_folder="/templates/room/")


@roombp.route("/state")
def roomstate():
    roomlist = list(Room.query.all())
    return render_template("room/state.html", roomname="room", roomlist=roomlist)


@roombp.route("/room/<string:roomname>")
def roomstatus(roomname):
    roomlist = list(Room.query.all())

    thisroomid = Room.query.filter(Room.roomname == roomname).first()
    if (thisroomid == None):
        flash("未找到此教室" + roomname, "warning")
        return render_template("error.html", errmsg="未找到此教室")

    model = {}
    model["date"] = []

    model["roomlist"] = roomlist  # 所有会议室
    model["roomname"] = roomname  # 当前会议室

    model["schedule"] = {}

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    today = datetime.date(year, month, day)  # datetime.date

    weekday, lastday = calendar.monthrange(year, month)
    weekday = weekday + 1  # 星期几

    schedulelist = Schedule.query.filter(Schedule.class_date >= today).filter(
        Schedule.class_date < today + datetime.timedelta(days=7)).filter(Schedule.room_id == thisroomid.id) \
        .order_by(Schedule.class_n).all()

    for i in range(7):
        model["date"].append(today + datetime.timedelta(days=i))

    for si in schedulelist:
        dayscha_delta = si.class_date - today  # datetime.timedelta
        dayscha = dayscha_delta.days  # 和今天相差几天

        # model["schedule"].append({"dayscha": dayscha, "class_n": si.class_n, "user": si.user.username})
        # model["schedule"].append({"dayscha": dayscha, "class_n": si.class_n, "user": si.user.username})
        model["schedule"][(dayscha, si.class_n)] = {"username":si.user.username,"useage":si.useage}

    for i in roomlist:
        if (roomname == i.roomname):
            return render_template("room/state.html", model=model)
    return render_template("error.html", errmsg="未找到此教室")


