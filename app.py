from flask import Flask, render_template, url_for, redirect, request, flash
from datetime import datetime
from model import create_app, Writeup, db, User
from get_time import get_time_left
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, WritingForm


#prevents error: working outside of the application context. To solve this, set up an application context with app.app_context()
app = create_app()
app.app_context().push()

#creating an instance of the login manager object
login_manager = LoginManager()
#binding to the flask application instance
login_manager.init_app(app)

#user loader callback that generates current user's id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#renders the home page
@app.route('/')
def index():
    return render_template('index.html')

#login page
@app.route('/login', methods = ['POST','GET'])
def login():
    #creates login form
    form = LoginForm()
    if form.validate_on_submit:
        #accepts form input
        user = User.query.filter_by(email = form.email.data).first()
        
        #makes sure password is hashed before login
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            #redirects the user to where they can add more writeups after they login
            return redirect(url_for('add_writeup'))
        
        #flash an error message for invalid input
        flash("Invalid Login details")
    return render_template('login.html', form=form)

#signup page
@app.route('/register', methods = ['POST','GET'])
def register():
    #creates signup form
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit:
            #collects form data and saves in database
            user = User(first_name =form.first_name.data,
                        last_name =form.last_name.data,
                        email =form.email.data,
                        password = generate_password_hash(form.password.data)
                        )
            
            #adds the new user's details to the User table
            db.session.add(user)
            db.session.commit()
            
            #redirects the user to login
            return redirect(url_for('login'))

#route to logout
@app.route('/logout', methods = ['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

#route to add more writeups
@app.route('/add', methods = ['POST','GET'])
def add_writeup():
    #creates a form to add more writeups
    form = WritingForm()
    if request.method == 'GET':
        return render_template('add_writeup.html',form=form)
    
    if request.method == 'POST':
        #identifies the current user
        user = current_user
        
        if form.validate_on_submit:
            #adds form data to database
            writing = Writeup(content=form.title.data, writer = user.id, completed=False, due_date=form.due_date.data)
            db.session.add(writing)
            
            #saves data
            db.session.commit()
            #redirects user to the writing list page after submission
            return redirect(url_for('tracker'))

#route that shows the list of writeups
@app.route('/list')
def tracker():
    #gets the time left to meet deadlines with an helper function
    message_dict = get_time_left()
    
    #selects the writeups to display by the current user's id
    writeups = Writeup.query.filter_by(writer = current_user.id)
    
    return render_template('list.html', writeups = writeups, message_dict=message_dict)

#updates the status of the writeup from "in progress" to "completed"
@app.route('/update/<int:writing_id>')
def update(writing_id):
    #selects the id of the writeup to be updated
    writing = Writeup.query.filter_by(id=writing_id).first()
    
    #changes the boolean value from False to True
    writing.completed = not writing.completed
    
    #saves the changes to the database
    db.session.commit()
    #redirects back to the list page
    return redirect(url_for('tracker'))

#deletes a writeup
@app.route('/delete/<int:writing_id>')
def delete(writing_id):
    #selects the id of the writeup to be deleted
    writing = Writeup.query.filter_by(id=writing_id).first()
    
    #deletes the writeup from the database
    db.session.delete(writing)
    
    #saves the changes to the database
    db.session.commit()
    #redirects back to the list page
    return redirect(url_for('tracker'))

#allows user to edit already saved information
@app.route('/edit/<int:writing_id>', methods=["GET", "POST"])
def edit(writing_id):
    #gets the id of the writeup
    writing = Writeup.query.filter_by(id=writing_id).first()
    
    if request.method == "POST":
        #gets the new data from the form
        writing.content = request.form['title']
        due_date = request.form['deadline']
        
        #changes the datetime format to python format
        date_in_system = datetime.strptime(due_date,  '%Y-%m-%dT%H:%M')
        writing.due_date = date_in_system
        
        #saves the data to the database
        db.session.commit()
        #redirects back to the list page
        return redirect(url_for('tracker'))
    else:
        return render_template('edit.html', writing_id=writing_id)

#creates the database and runs the app to make it work 
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    
