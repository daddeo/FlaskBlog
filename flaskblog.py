# url_for: finds the exact location of routes for us, so we don't need to worry about it in the background
# 
from flask import Flask, escape, request, render_template, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
