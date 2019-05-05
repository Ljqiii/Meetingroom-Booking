from flask import Blueprint, render_template, flash, redirect,url_for
from flask_login import login_user, login_required, current_user, logout_user

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

        if (User.query.filter_by(username=username).first() != None):
            return render_template("error.html", errmsg="用户已存在,请直接登陆!")
        if(username=="admin"):
            adminrole = Role.query.filter_by(role_name="admin").first()
            user = User(username="admin", role_id=adminrole.id, isactive=True)
        else:
            user = User(username=username, role_id=role, isactive=not allrolelist[str(role)])
        user.setpassword(password)
        db.session.add(user)
        db.session.commit()

        u = User.query.filter_by(username=username).first()
        if (u.is_active == False):
            return render_template("unactive.html", needactive=True)
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
        if (user.is_active == False):
            return render_template("unactive.html")

        login_user(user, remember)
        return redirect(url_for("index"))
    return render_template("login.html", form=loginform)


@authbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@authbp.route("/me")
@login_required
def me():
    print(current_user)
    if(current_user.username=="admin" or current_user.role.role_name=="admin"):
        return redirect(url_for("admin.admin"))
    return render_template("me.html")


@authbp.route("/nopermission")
@login_required
def nopermission():
    return render_template("admin/permissiondenied.html")



@authbp.route("/unactive")
def unactive():
    if(current_user!=None):
        return redirect(url_for("auth.me"))
    return render_template("unactive.html")
