import os
from flask import Flask, send_from_directory, render_template, request, abort, session, redirect, flash, jsonify
import secrets, db
from werkzeug.utils import secure_filename
import string, random

s = string.ascii_letters

dbh = db.DbHelper()

app = Flask("Bolg",
            template_folder='html_files',
            static_folder="static",
            static_url_path="/static")

app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['PERMANENT_SESSION_LIFETIME'] = 43200  # seconds, which equalize to 30 days.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = 'static/images/upload'


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/favicon.ico')
def favicon():
    # website's icon
    return send_from_directory(os.path.join(app.root_path, 'icons'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect('/login', 302)
        return "oh u bad boy"
    else:
        return render_template("index.html")


@app.route('/contact')
def contact_page():
    return render_template('contact.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':

        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return error("You already logged in !")
    elif request.method == "POST":

        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            flash('Welcome back!')
            return redirect("/", 302)
        else:
            flash('Invalid creds!')
            return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/", 302)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/post', methods=['get', 'post'])
def post():
    if not session.get('logged_in'):
        return redirect('/login', 302)
        return "oh u bad boy"

    if request.method == "POST":

        file = request.files['file']
        if allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            title = request.form['title']
            body = request.form['body']

            dbh.add_blog(title, body, '/'+path)

            return redirect("/", 301)

        else:
            return error('Invalid file')
    elif request.method == "GET":
        return render_template('post.html')





@app.errorhandler(404)
def notfound(x):

    return f"<h1><center>{x}</center></h1>"


#######################################################################################################################

@app.route('/api/get_posts')
def get_posts():
    return jsonify(dbh.get_blogs())


def error(err):
    return f"<h1><center>{err}</center></h1>"


app.run(host="127.0.0.1", port=80, debug=True)
