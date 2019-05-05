from Model import Notification, db
from flask_login import current_user
from flask import flash


def newnoti(to_user, msg):
    noti = Notification(to_user=to_user, msg=msg)
    db.session.add(noti)
    db.session.commit()


def deletenoti(notification_id):
    n = Notification.query.filter_by(id=notification_id).filter_by(to_user=current_user.id).first()
    if (n != None):
        db.session.delete(n)
        db.session.commit()
        flash("删除成功","warning")

def markasread(notification_id):
    n = Notification.query.filter_by(id=notification_id).filter_by(to_user=current_user.id).first()
    if (n != None):
        n.isread = True
        db.session.add(n)
        db.session.commit()
        flash("已标为已读", "warning")

