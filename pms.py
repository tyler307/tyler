from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path='')
app.debug =True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/personal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True





db = SQLAlchemy(app)   #创建数据库核心对象


# from personal.views import employee
# app.register_blueprint(employee,url_prefix="/emp") #注册employee蓝图，添加前缀/emp
from personal.views import emp
app.register_blueprint(emp,url_prefix="/admin")


@app.route('/')
def index():
    return 'Index'

@app.route('/admin/')
def admin_index():
    return render_template('admin/layout.html')

if __name__ == '__main__':
    app.run()
