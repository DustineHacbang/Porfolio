from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
#connects model information to controller
from flask_app.models.users import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/users")
    return render_template("index.html")


@app.route("/users")
def display_users():
    if "user_id" not in session:
        flash("Must log in")
        return redirect('/')
    return render_template(
        "display_page.html", all_users = User.get_all(), user = User.get_by_id({"id": session['user_id']})
        )


@app.route("/register", methods = ["POST"])
def register():
    if not User.register_validate(request.form):
        return redirect("/")    
    lee = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": lee
    }
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/users")


@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validate(request.form):
        return redirect("/")    
    user = User.get_by_email({"email": request.form['email']})
    # user_id = unique users id
    session['user_id'] = user.id
    return redirect("/users")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")