from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.debug = True
app.config ['SECRET_KEY'] = 'authappsecretkey'
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def redirect_to_register():
    """Redirect to registration form"""

    return redirect('/register')

@app.route('/register')
def show_registration_form():
    """Show the registration form
       Don't show if user is already logged in"""
    
    if "user" in session:
        logged_in_user = session.get('user')
        
        return redirect(f'/users/{logged_in_user}')

    form = RegistrationForm()

    return render_template('register.html', form=form)

@app.route('/register', methods=["POST"])
def handle_registration_form():
    """Process the registration form and redirect to user page
       Don't show if user is already logged in"""

    if "user" in session:
        logged_in_user = session.get('user')

        return redirect(f'/users/{logged_in_user}')

    form = RegistrationForm()

    #get form data and create new User instance and save to database
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        #create hashed password
        new_user = User.register(username, password, email, first_name, last_name)

        #save to database
        db.session.add(new_user)
        db.session.commit()

        session['user', new_user.username]

        return redirect(f'/users/{username}')
    

    return render_template('register.html', form=form)


@app.route('/login')
def show_login_form():
    """Show login form
       Don't show if user is already logged in"""

    if "user" in session:
        logged_in_user = session.get('user')

        return redirect(f'/users/{logged_in_user}')
    
    form = LoginForm()

    return render_template('login.html', form=form)

@app.route('/login', methods=["POST"])
def handle_login_form():
    """Process login form and redirect to user secrete page
       Don't show if user is already logged in"""

    if "user" in session:
        logged_in_user = session.get('user')

        return redirect(f'/users/{logged_in_user}')

    form = LoginForm()

    #get form data
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['user'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user_page(username):
    """Show the user info page"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only look at your own info!")
        return redirect(f'/users/{logged_in_user}')
    
    feedback = Feedback.query.filter_by(username=username).all()
    page_user = User.query.get_or_404(username)
    
    return render_template('user_info.html', user=page_user, feedback=feedback)


@app.route('/logout')
def logout_user():
    """Log the current user out of the session"""

    session.pop('user')
    return redirect('/')

@app.route('/users/<username>/delete')
def delete_user(username):
    """Delete user from database
       Cascasde to delete all feedback
       clear session and redirect to home"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only delete your own account!")
        return redirect(f'/users/{logged_in_user}')

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<username>/feedback/add')
def show_feedback_form(username):
    """show the add feedback form"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only add feedback to your own profile.")
        return redirect(f'/users/{logged_in_user}')
    
    form = FeedbackForm()
    page_user = User.query.get_or_404(username)
    
    return render_template('feedback_form.html', form=form, user=page_user)

@app.route('/users/<username>/feedback/add', methods=["POST"])
def handle_feedback_form(username):
    """show the add feedback form"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)
    
    if logged_in_user != username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only add feedback to your own profile.")
        return redirect(f'/users/{logged_in_user}')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        page_user = User.query.get_or_404(username)

        new_feedback = Feedback(title=title, 
                                content=content,
                                username=page_user.username)
        db.session.add(new_feedback)
        db.session.commit()

    return redirect(f'/users/{username}')

@app.route('/feedback/<feedback_id>')
def show_feedback_detail(feedback_id):
    """Show detailed feedback page"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)

    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != feedback.username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only see feedback on your own profile.")
        return redirect(f'/users/{logged_in_user}')
    
    return render_template('feedback_detail.html', feedback=feedback)

@app.route('/feedback/<feedback_id>/update')
def show_update_feedback_form(feedback_id):
    """show the edit feedback form"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)
        
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != feedback.username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only edit feedback on your own profile.")
        return redirect(f'/users/{logged_in_user}')

    form = FeedbackForm()
    form.title.data = feedback.title
    form.content.data = feedback.content

    return render_template('edit_feedback.html', feedback=feedback, form=form)

@app.route('/feedback/<feedback_id>/update', methods=["POST"])
def handle_update_feedback_form(feedback_id):
    """show the edit feedback form"""

    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)

    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != feedback.username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only edit feedback on your own profile.")
        return redirect(f'/users/{logged_in_user}')
    
    form = FeedbackForm()
    feedback.title = form.title.data
    feedback.content = form.content.data
    db.session.commit()

    return redirect(f'/users/{logged_in_user}')

@app.route('/feedback/<feedback_id>/delete')
def delete_feedback(feedback_id):
    """delete individual piece of feedback"""
    if "user" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)
    logged_in_user = session.get('user')
    logged_in_user_DB = User.query.get_or_404(logged_in_user)

    if logged_in_user != feedback.username and not logged_in_user_DB.is_admin:
        flash("Oops, you can only delete your own feedback!")
        return redirect(f'/users/{logged_in_user}')
    
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{logged_in_user}')
