from flask import Blueprint, render_template,url_for,redirect,request
from flask.views import MethodView
from pms import db
from .models import *
from datetime import datetime

# employee = Blueprint('employee', __name__)  # 创建蓝图
emp = Blueprint('emp', __name__)


# # 创建基于方法的类
# class EmployeeListView(MethodView):
#     def get(self):
#         employees = db.session.query(Employee).all()[:10]
#         return render_template('employee-list.html', employees=employees)
#
#
# # 添加url地址
# employee.add_url_rule('/list/', view_func=EmployeeListView.as_view('employee_list_view'))


class EmpList(MethodView):
    def get(self):
        employees = db.session.query(Employee).limit(20)
        # employees = db.session.query(Employee).filter_by(id=541)
        return render_template('admin/emp-list.html', employees=employees)


emp.add_url_rule('/emp/emp-list/', view_func=EmpList.as_view('emp-list'))


class EmpListDel(MethodView):
    def get(self, id=None):
        if id:
            employee = db.session.query(Employee).get(id)
            if employee:
                db.session.delete(employee)
                db.session.commit()
        return redirect(url_for('emp.emp-list'))

emp.add_url_rule('/emp/del/<id>/',view_func=EmpListDel.as_view('emp-del'))

class EmpListCreateorEdit(MethodView):
    def get(self):
        id = request.args.get('id',None)
        if id:
            employee = db.session.query(Employee).get(id)
            departments = db.session.query(Department).all()
            if employee:
                return render_template('admin/emp-edit.html',employee = employee,departments = departments)
            else:
                return redirect(url_for('emp.emp-list'))
        else:
            departments = db.session.query(Department).all()
            return render_template('admin/emp-detail.html',departments = departments)

    def post(self):
        id = int(request.form.get('id'))
        if id:
            employee = db.session.query(Employee).get(id)

            employee.name = request.form.get('name')
            employee.gender = request.form.get('gender')
            employee.job = request.form.get('job')
            employee.birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d')
            employee.idCard = request.form.get('idCard')
            employee.address = request.form.get('address')
            employee.salary = float(request.form.get('salary'))
            employee.department_id = request.form.get('department_id')
            # employee.release_time = datetime.now()

            db.session.commit()

            return redirect(url_for('emp.emp-list'))
        else:
            employee = Employee(
            request.form.get('name'),
            request.form.get('gender'),
            request.form.get('job'),
            datetime.strptime(request.form.get('birthdate'),'%Y-%m-%d'),
            request.form.get('idCard'),
            request.form.get('address'),
            float(request.form.get('salary'))
            )

            employee.department_id = request.form.get('department_id')
            employee.release_time = datetime.now()

            db.session.add(employee)
            db.session.commit()

            return redirect(url_for('emp.emp-list'))

emp.add_url_rule('/emp/edit/',view_func=EmpListCreateorEdit.as_view('emp-detail'))