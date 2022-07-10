from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm,SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
import os



@app.route('/',methods = ['POST','GET'])
def home():
    return render_template('home.html')


#This is the index route where we are going to
#query on all our employee data
@app.route('/Crud')
def Crud():
    all_data = User.query.all()

    return render_template("Crud.html", Users = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        email = request.form['email']
        username = request.form['username']
        registration_number = request.form['registration_number']
        Role = request.form['Role']
        password_hash = request.form['password_hash']


        my_data = User( email,username,registration_number,Role,password_hash)
        db.session.add(my_data)
        db.session.commit()

        flash("User Inserted Successfully")

        return redirect(url_for('Crud'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.email = request.form['email']
        my_data.username = request.form['username']
        my_data.registration_number = request.form['registration_number']
        my_data.Role = request.form['Role']
        my_data.password_hash = request.form['password_hash']

        db.session.commit()
        flash("User Updated Successfully")

        return redirect(url_for('Crud'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('Crud'))










@app.route('/SearchEngine')
def SearchEngine():
    form = SearchForm()
    #return render_template('SearchEngine.html', form=form)

    if form.validate_on_submit():
        new_eq = Equipment(name = form.name.data)
        if form.manual.data:
            manual_path = join(
                app.config['UPLOADED_MANUALS_DEST'],
                secure_filename(form.manual.data.filename)
                )

            form.manual.data.save(manual_path)
            new_eq.manual_path = manual_path

        db.session.add(new_eq)
        db.session.commit()

    return render_template('SearchEngine.html', form=form)





@app.route('/Test',methods=['GET', 'POST'])
def Test():
    #next = url_for('Test')
    #return redirect(next)
    return render_template('Test.html')



@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                form2 = SearchForm()
                next = url_for('SearchEngine',form2=form2)

            return redirect(next)
    return render_template('login.html', form=form)
















@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    registration_number=form.registration_number.data,
                    Role=form.Role.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)





@app.route('/index')
def index():
    path = "C:/Users/Samar/Desktop/5BI4"
    dirs = os.listdir(path)
    temp = []
    for dir in dirs:
        if dir.endswith('.pdf'):
            temp.append({'name': dir})

    return render_template('index.html', data=temp )

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    print(select)
    return(str(select)) # just to see what select is









if __name__ == '__main__':
    app.run(debug=True)
