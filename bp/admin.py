from flask import Blueprint, render_template, flash, redirect, url_for,request
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
    return render_template("admin/roommanage.html")


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
        if(request.method=="POST"):
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
    pass
