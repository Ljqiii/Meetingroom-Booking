from amqp.spec import method
from flask import Blueprint, render_template, flash, redirect, request, url_for
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

    loginform = Login()

    roomlist = list(Room.query.all())

    thisroomid = Room.query.filter(Room.roomname == roomname).first()
    if (thisroomid == None):
        flash("未找到此教室" + roomname, "warning")
        return render_template("error.html", errmsg="未找到此教室")

    model = {}
    model["date"] = []

    model["roomlist"] = roomlist  # 所有会议室
    model["room"] = {"roomname": roomname, "roomid": thisroomid.id, "needactive": thisroomid.need_active}

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

        model["schedule"][(dayscha, si.class_n)] = {"username": si.user.username, "useage": si.useage}

    for i in roomlist:
        if (roomname == i.roomname):
            return render_template("room/state.html", model=model,form=loginform)
    return render_template("error.html", errmsg="未找到此教室")


@login_required
@roombp.route("/booking/", methods=["POST"])
def bookaroom():
    roomname = request.form["roomname"]
    classn = request.form["classn"]
    daysdelta = int(request.form["daysdelta"])
    useage = request.form["useage"]

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    today = datetime.date(year, month, day)

    class_date = today + datetime.timedelta(days=daysdelta)

    room = Room.query.filter_by(roomname=roomname).first()
    if (room == None):
        return render_template("error.html", "房间未找到")
    else:
        s = Schedule(user_id=current_user.id, room_id=room.id, class_n=classn, class_date=class_date, useage=useage,
                     is_active=not room.need_active)
        db.session.add(s)
        db.session.commit()
        if (room.need_active):
            flash("等待管理员审核", "warning")
        else:
            flash("预定成功", "success")

        return redirect(url_for("room.roomstatus", roomname=roomname))
