from flask_login import UserMixin
from sqlalchemy.dialects.mssql import TINYINT
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# 教室
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    roomname = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.VARCHAR(20), nullable=True)

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    department = db.relationship("Department", lazy=True)
    # 此教室被预定的人
    user = db.relationship("User", secondary="schedule")

    __table_args__ = {
        'mysql_charset': "utf8"
    }

    def __repr__(self):
        return '<Room %r:%r>' % self.id, self.roomname


# 预定
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))

    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)

    useage = db.Column(db.VARCHAR(300), nullable=True)



    __table_args__ = {
        'mysql_charset': "utf8"
    }


# 系
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.VARCHAR(10), nullable=False)

    room = db.relationship("Room", lazy=True)

    __table_args__ = {
        'mysql_charset': "utf8"
    }

    def __repr__(self):
        return "<Department %r>" % self.department_name


# 角色 admin 教师,系主任,管理
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.VARCHAR(20), default=0, nullable=True)
    need_actice = db.Column(db.Boolean, default=0, nullable=False)

    def __repr__(self):
        return "<Role %r>" % self.role_name

    __table_args__ = {
        'mysql_charset': "utf8"
    }


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    to_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    msg = db.Column(db.VARCHAR(50), nullable=False)

    isread = db.Column(db.Boolean, nullable=True, default=False)

    __table_args__ = {
        'mysql_charset': "utf8"
    }

    def __repr__(self):
        return "<Notification to %r, msg %r>" % self.name, self.msg


# 用户
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.VARCHAR(20), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    password_hash = db.Column(db.String(128), nullable=False)
    isactive = db.Column(db.Boolean, nullable=False)

    # 用户角色
    role = db.relationship("Role", lazy=True)
    # 已经预定的教室
    roombooked = db.relationship("Room", secondary="schedule")

    __table_args__ = {
        'mysql_charset': "utf8"
    }

    def __repr__(self):
        return "<User %r>" % self.username

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return bool(self.isactive)
        # return True

    def get_id(self):
        return str(self.id)

    def setpassword(self, password):
        self.password_hash = generate_password_hash(password)
