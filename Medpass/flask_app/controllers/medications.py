from flask_app import app
from flask import render_template, redirect, request, session
#connects model information to controller
from flask_app.models.users import User
from flask_app.models.medications import Medications

@app.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    all_medications = Medications.get_all()
    return render_template('display_page.html', user = logged_user, all_medications = all_medications)

@app.route('/medication/<int:medication_id>')
def medication_info(medication_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    medication = Medications.get_by_id({'id':medication_id})
    logged_user = User.get_by_id({'id': session['user_id']})
    if not medication:
        return redirect('/dashboard')
    return render_template('medication_detail.html', medication = medication, user = logged_user)



@app.route('/new')
def new_medication():
    # if 'user_id' not in session:
    #     return redirect('/')
    return render_template('new_medication.html')



@app.route('/create', methods=['POST'])
def create_medication():
    if not Medications.medication_validate(request.form):
        return redirect('/new') 
    medication = {
        'instructions':request.form['instructions'],
        'side_effects':request.form ['side_effects'],
        'given_date':request.form ['given_date'],
        'expiration_date':request.form ['expiration_date'],
        'user_id':session['user_id'],
    }
    Medications.create(medication)
    return redirect('/dashboard')



@app.route('/edit/<int:medications_id>')
def edit_medication(medications_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    medications_to_edit = Medications.get_by_id({ 'id': medications_id})
    if not medications_to_edit:
        return redirect('/display_page')
    return render_template('edit_medication.html', medications = medications_to_edit)



@app.route('/update/<int:medications_id>', methods=['POST','GET'])
def update_medication(medications_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    if not Medications.medication_validate(request.form):
        return redirect(f'/edit/{medications_id}')
    data = {
        'id': medications_id,
        'instructions': request.form['instructions'],
        'side_effects': request.form['side_effects'],
        'expiration_date': request.form['expiration_date'],
        'given_date': request.form['given_date'],
        
    }
    Medications.update_one(data)
    return redirect('/dashboard')



@app.route('/delete/<int:medications_id>')
def delete_medication(medications_id):
    # if 'user_id' not in session:
    #     return redirect('/')    
    Medications.delete({ 'id': medications_id })
    return redirect('/dashboard')