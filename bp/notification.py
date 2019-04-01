from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import login_user, login_required, current_user, logout_user

from Form import Register, Role, Login
from Model import db, Notification

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
    n = Notification.query.filter_by(id=notification_id).filter_by(to_user=current_user.id).first()
    if (n != None):
        n.isread = True
        db.session.add(n)
        db.session.commit()
        flash("已标为已读","warning")
    return (redirect(url_for("notification.notification")))
