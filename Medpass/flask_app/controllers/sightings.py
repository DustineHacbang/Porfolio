from flask_app import app
from flask import render_template, redirect, request, session
#connects model information to controller
from flask_app.models.users import User
from flask_app.models.medication import Medications

@app.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    all_meds = Medications.get_all()
    return render_template('display_page.html', user = logged_user, all_meds = all_meds)

@app.route('/med/<int:meds_id>')
def medication_info(meds_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    med = Medications.get_by_id({'id':meds_id})
    logged_user = User.get_by_id({'id': session['user_id']})
    if not med:
        return redirect('/dashboard')
    return render_template('med_info.html', med = med, user = logged_user)



@app.route('/new')
def new_medications():
    # if 'user_id' not in session:
    #     return redirect('/')
    return render_template('med_medication.html')



@app.route('/create', methods=['POST'])
def create_medication():
    if not Medications.medication_validate(request.form):
        return redirect('/new') 
    medication = {
        'instruction':request.form['instruction'],
        'expiration_date':request.form ['expiration_date'],
        'side_effects':request.form ['side_effects'],
        'num_dosage':request.form ['num_dosage'],
        'user_id':session['user_id'],
    }
    Medications.create(medication)
    return redirect('/dashboard')



@app.route('/edit/<int:meds_id>')
def edit_medication(meds_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    meds_to_edit = Medications.get_by_id({ 'id': meds_id})
    if not meds_to_edit:
        return redirect('/display_page')
    return render_template('edit_medication.html', meds = meds_to_edit)



@app.route('/update/<int:meds_id>', methods=['POST','GET'])
def update_medication(meds_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    if not Medications.medication_validate(request.form):
        return redirect(f'/edit/{meds_id}')
    data = {
        'instruction':request.form['instruction'],
        'expiration_date':request.form ['expiration_date'],
        'side_effects':request.form ['side_effects'],
        'num_dosage':request.form ['num_dosage'],
        'user_id':session['user_id'],
        
    }
    Medications.update_one(data)
    return redirect('/dashboard')



@app.route('/delete/<int:meds_id>')
def delete_medication(meds_id):
    # if 'user_id' not in session:
    #     return redirect('/')    
    Medications.delete({ 'id': meds_id })
    return redirect('/dashboard')