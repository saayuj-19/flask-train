from flask import Flask, render_template, request, redirect, abort
from flasktrain.models import db, EmployeeModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables before the first request in Flask 2.x
with app.app_context():
    db.create_all()

@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')

@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)

@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    
    return f"Employee with id = {id} Doesn't exist"

@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if not employee:
        return f"Employee with id = {id} Does not exist"

    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()

        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect(f'/data/{id}')

    return render_template('update.html', employee=employee)

@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if not employee:
        abort(404)

    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect('/data')

    return render_template('delete.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)