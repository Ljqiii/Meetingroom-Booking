from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import login_user, login_required, current_user, logout_user

from Form import Register, Role, Login
from Model import db, Notification
from utils import notificationutil
notificationbp = Blueprint("notification", __name__, static_folder='static', static_url_path="/static",
                           template_folder="templates")


@notificationbp.route("/notification")
@login_required
def notification():
    n = Notification.query.filter_by(to_user=current_user.id).order_by(Notification.isread).all()
    return render_template("notification.html", notifications=n)


@notificationbp.route("/markread/<int:notification_id>")
@login_required
def markread(notification_id):
    notificationutil.markasread(notification_id)
    return (redirect(url_for("notification.notification")))


@notificationbp.route("/delete/<int:notification_id>")
@login_required
def delete(notification_id):
    notificationutil.deletenoti(notification_id)
    return (redirect(url_for("notification.notification")))
