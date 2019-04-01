from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField

from Model import Role
from wtforms.validators import DataRequired, Email, Length, EqualTo


class Register(FlaskForm):
    role = SelectField("角色")
    #
    # name = StringField("姓名", validators=[DataRequired(), Length(2, 20)])
    username = StringField("用户名", validators=[DataRequired(), Length(2, 20, message="用户名必须在6-20字符之间")])
    password = PasswordField("密码", validators=[DataRequired(), Length(6, 20, message="密码必须在6-20字符之间")])
    repeatpassword = PasswordField("重复密码",
                                   validators=[DataRequired(), EqualTo("password", message="密码不一致")])

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.role.choices = [(str(i.id), str(i.role_name)) for i in Role.query.all()]


class Login(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(2, 20)])
    password = PasswordField("密码", validators=[DataRequired(), Length(6, 20, message="密码必须在6-20字符之间")])
    remember = BooleanField("记住我")
    submit = SubmitField("提交")


class BookRoom(FlaskForm):
    roomname = StringField("房间名", validators=[DataRequired(), Length(1, 20)])
    starttime = StringField("开始时间", validators=[DataRequired()])
    endtime = StringField("结束时间", validators=[DataRequired()])
    comment = StringField("使用", validators=[DataRequired()])
