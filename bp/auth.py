from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, login_required, current_user

from Form import Register, Role, Login
from Model import User, db

authbp = Blueprint("auth", __name__, static_folder='static', static_url_path="/static", template_folder="templates")


@authbp.route("/register", methods=["GET", "POST"])
def registerfun():
    regform = Register()

    if (regform.validate_on_submit()):
        # name = regform.name.data
        username = regform.username.data
        password = regform.password.data
        role = regform.role.data

        allrolelist = {str(i.id): i.need_actice for i in Role.query.all()}

        if (role not in allrolelist.keys()):
            return render_template("error.html", errmsg="角色不存在!")

        print("role: " + role)

        if (User.query.filter_by(username=username).first() != None):
            return render_template("error.html", errmsg="用户已存在,请重新注册!")

        user = User(username=username, role_id=role, isactive=not allrolelist[str(role)])
        user.setpassword(password)
        db.session.add(user)
        db.session.commit()

        u = User.query.filter_by(username=username).first()
        login_user(u)

        print(username, password)
        flash("注册成功!")
        return redirect("me")

    else:
        for field, errors in regform.errors.items():
            print(field, errors)
            flash(errors[0])
        haveadmin = False
        if (User.query.filter_by(username="admin").first() == None):
            haveadmin = True
        return render_template("register.html", form=regform, nothaveadmin=haveadmin)


@authbp.route("/hadmin", methods=["GET"])
def aadmin():
    haveadmin = User.query.filter_by(username="admin").first()
    return str(haveadmin)


@authbp.route("/addrole", methods=["GET"])
def addrole():
    role1 = Role(id="1", role_name="11", need_actice=True)
    role2 = Role(id="2", role_name="22", need_actice=False)

    db.session.add(role1)
    db.session.add(role2)
    db.session.commit()


@authbp.route("/login", methods=["GET", "POST"])
def login():
    loginform = Login()
    if (loginform.validate_on_submit()):
        username = loginform.username.data
        password = loginform.password.data
        remember = loginform.remember.data

        user = User.query.filter_by(username=username).first()
        if (user == None or not user.validate_password(password)):
            return render_template("error.html", errmsg="用户名或密码错误!")

        login_user(user, remember)
        return redirect("me")
    return render_template("login.html", form=loginform)


@authbp.route("/me")
@login_required
def me():
    print(current_user)
    return render_template("me.html")
