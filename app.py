from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm,SearchForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/',methods = ['POST','GET'])
def home():
    form = SearchForm()
    return render_template('home.html',form=form)


#__________________________________show list_____________________________________________________#
@app.route('/data')
def RetrieveDataList():
    Users = User.query.all()
    return render_template('Results.html',Users = Users)

@app.route('/Results',methods=['GET'])
def Results():
    #next = url_for('Test')
    #return redirect(next)
    return render_template('Results.html')

#____________________________________________retrieve a specific user________________________________________#
@app.route('/data/<int:registration_number>')
def RetrieveSingleUser(registration_number):
    user = User.query.filter_by(registration_number=registration_number).first()
    if user:
        return render_template('Data.html', user = user)
    return f"user with username ={registration_number} Doenst exist"

@app.route('/Data',methods=['GET'])
def Data():
    #next = url_for('Test')
    #return redirect(next)
    return render_template('Data.html')


#______________________________________________Update____________________________________________________________________#

@app.route('/data/<int:registration_number>/update',methods = ['GET','POST'])
def update(registration_number):
    user = User.query.filter_by(registration_number=registration_number).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()

            email = request.form['email']
            username = request.form['username']
            Role = request.form['Role']
            password = request.form['password']
            user = User(registration_number=registration_number, email=email, username = username, Role=Role,password=password)

            db.session.add(user)
            db.session.commit()
            return redirect(f'/data/{registration_number}')
        return f"User with id = {registration_number} Does nit exist"

    return render_template('Update.html', user = user)

@app.route('/Update',methods=['GET','POST'])
def Update():
    #next = url_for('Test')
    #return redirect(next)
    return render_template('Update.html')



####Delete a user####
@app.route('/data/<int:registration_number>/delete', methods=['GET','POST'])
def delete(registration_number):
    user = User.query.filter_by(registration_number=registration_number).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html',user = user)

@app.route('/delete',methods=['GET','POST'])
def delette():
    #next = url_for('Test')
    #return redirect(next)
    return render_template('delete.html')



#________________________________________Crud__________________________________#
@app.route("/Crud", methods=['GET', 'POST'])
def Crud():

    if request.method == 'GET':
        if request.form.get('action1') == 'VALUE1':
            return render_template('Results.html')
        else:
            return render_template('Crud.html')
    #elif request.method == 'GET':
        #return render_template('Crud.html')

    return render_template("Crud.html")

@app.route('/Crud',methods=['GET','POST'])
def Crudd():
    form = CrudForm()
    #next = url_for('Test')
    #return redirect(next)
    return render_template('Crud.html',form= form)









@app.route('/SearchEngine')
def SearchEngine():
    form = SearchForm()
    #return render_template('SearchEngine.html', form=form)

    if form.validate_on_submit():

        return redirect(url_for('welcome_user'))
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

if __name__ == '__main__':
    app.run(debug=True)




@app.route('/Search')
def Search():
    return '<h1>Hello Puppy!</h1>'
