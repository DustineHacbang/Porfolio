from flask_app import app
from flask import render_template, redirect, request, session
#connects model information to controller
from flask_app.models.users import User
from flask_app.models.sightings import Sightings

@app.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    all_reports = Sightings.get_all()
    return render_template('display_page.html', user = logged_user, all_reports = all_reports)

@app.route('/report/<int:reports_id>')
def sighting_info(reports_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    report = Sightings.get_by_id({'id':reports_id})
    logged_user = User.get_by_id({'id': session['user_id']})
    if not report:
        return redirect('/dashboard')
    return render_template('sighting_report.html', report = report, user = logged_user)



@app.route('/new')
def new_sightings():
    # if 'user_id' not in session:
    #     return redirect('/')
    return render_template('report_sighting.html')



@app.route('/create', methods=['POST'])
def create_sighting():
    if not Sightings.sighting_validate(request.form):
        return redirect('/new') 
    sighting = {
        'location':request.form['location'],
        'what_happened':request.form ['what_happened'],
        'sighting_date':request.form ['sighting_date'],
        'num_saquaches':request.form ['num_saquaches'],
        'user_id':session['user_id'],
    }
    Sightings.create(sighting)
    return redirect('/dashboard')



@app.route('/edit/<int:reports_id>')
def edit_sighting(reports_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    reports_to_edit = Sightings.get_by_id({ 'id': reports_id})
    if not reports_to_edit:
        return redirect('/display_page')
    return render_template('edit_sighting.html', reports = reports_to_edit)



@app.route('/update/<int:reports_id>', methods=['POST','GET'])
def update_sighting(reports_id):
    # if 'user_id' not in session:
    #     return redirect('/')
    if not Sightings.sighting_validate(request.form):
        return redirect(f'/edit/{reports_id}')
    data = {
        'id': reports_id,
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'num_saquaches': request.form['num_saquaches'],
        'sighting_date': request.form['sighting_date'],
        
    }
    Sightings.update_one(data)
    return redirect('/dashboard')



@app.route('/delete/<int:reports_id>')
def delete_sighting(reports_id):
    # if 'user_id' not in session:
    #     return redirect('/')    
    Sightings.delete({ 'id': reports_id })
    return redirect('/dashboard')