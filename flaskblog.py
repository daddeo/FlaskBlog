# url_for: finds the exact location of routes for us, so we don't need to worry about it in the background
# 
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# python -> import secrets -> secrets.token_hex(16)
app.config['SECRET_KEY'] = '57383f18a431c57cc60880218eff93c6'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# route is used to navigate to different pages
@app.route('/')
def greeting():
    name = request.args.get("name", "World")
    return f'<h1>Hello, {escape(name)}!</h1><p>homepage</p>'

@app.route('/home')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash(f"You have been logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash(f"Login failed. Please check username and password.", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
