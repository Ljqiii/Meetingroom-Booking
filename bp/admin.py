from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from Form import *
from Model import *

adminbp = Blueprint("admin", __name__, static_folder='static', static_url_path="/static",
                    template_folder="/templates/admin/", url_prefix="/admin")


@adminbp.before_request
def verificationadmin():
    if (current_user.username != "admin" or current_user.role.role_name != "admin"):
        return redirect(url_for("auth.nopermission"))


@adminbp.route("/")
@login_required
def admin():
    departmentform = AddDepartment()
    return render_template("admin/adminindex.html", departmentform=departmentform)


@adminbp.route("/roommanage")
@login_required
def roommanage():
    return render_template("admin/roommanager.html")


@adminbp.route("/manage/room", methods=["GET", "POST"])
@login_required
def roommanager():
    pass


@adminbp.route("/manage/departmentmanager", methods=["GET", "POST"])
@login_required
def departmentmanager():
    departmentform = AddDepartment()
    if (departmentform.validate_on_submit()):
        departmentname = departmentform.department_name.data
        try:
            department = Department(department_name=departmentname)
            db.session.add(department)
            db.session.commit()
            flash("添加成功", "success")
        except:
            flash("添加失败", "danger")
    else:
        if (request.method == "POST"):
            flash("数据验证失败", "danger")

    departmentlist = Department.query.all()
    return render_template("admin/departmentmanager.html", form=departmentform, list=departmentlist)


@adminbp.route("/manage/deldepartment/<int:id>", methods=["GET"])
@login_required
def deldepartment(id):
    try:
        department = Department.query.filter_by(id=id).first()
        db.session.delete(department)
        db.session.commit()
        flash("删除成功", "success")
    except:
        flash("删除失败", "danger")
    return redirect(url_for("admin.departmentmanager"))


@adminbp.route("/manage/changepasswd", methods=["GET", "POST"])
@login_required
def changepasswd():
    form = ChangePasswd()
    if (form.validate_on_submit()):
        u = form.username.data
        p = form.password.data
        user = User.query.filter_by(username=u).first()
        if (user == None):
            flash("用户不存在", "warning")
        else:
            user.setpassword(p)
            db.session.add(user)
            db.session.commit()

            flash("修改" + u + "的密码成功", "success")
        return redirect(url_for("admin.changepasswd"))
    else:
        return render_template("admin/passwdmanager.html", form=form)


@adminbp.route("/manage/unactiveuser", methods=["GET", "POST"])
@login_required
def unactiveusermanager():
    unactive_user_list = User.query.filter_by(isactive=False).all()
    return render_template("admin/unactiveusermanager.html",userlist=unactive_user_list)


@adminbp.route("/manage/active/<int:userid>", methods=["GET"])
@login_required
def activeuser(userid):
    user = User.query.filter_by(id=userid).filter_by(isactive=False).first()
    if (user == None):
        flash("用户不存在", "warning")
    else:
        user.isactive = True
        db.session.add(user)
        db.session.commit()
        flash("激活用户成功", "success")
    return redirect(url_for("admin.unactiveusermanager"))

@adminbp.route("/manage/delete/<int:userid>", methods=["GET"])
@login_required
def deleteuser(userid):
    user = User.query.filter_by(id=userid).filter_by(isactive=False).first()
    if (user == None):
        flash("用户不存在", "warning")
    else:
        user.isactive = True
        db.session.delete(user)
        db.session.commit()
        flash("删除用户成功", "success")
    return redirect(url_for("admin.unactiveusermanager"))
