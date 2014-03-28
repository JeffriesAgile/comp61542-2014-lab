from string import replace
from comp61542 import app, mail, login_manager
from database import database, models
from visualization import network
from flask import (render_template, request, send_file, flash, redirect, abort, url_for)
from werkzeug import exceptions
from flask_mail import Message
from forms import forms
from flask_login import login_required, login_user, logout_user


def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([(fmt % i).rstrip('0').rstrip('.') for i in item]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route("/averages", methods=['GET', 'POST'])
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE]
    tables.append({
        "id": 1,
        "title": "Average Authors per Publication",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_per_publication(i)[1])
            for i in averages]})
    tables.append({
        "id": 2,
        "title": "Average Publications per Author",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_per_author(i)[1])
            for i in averages]})
    tables.append({
        "id": 3,
        "title": "Average Publications in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_in_a_year(i)[1])
            for i in averages]})
    tables.append({
        "id": 4,
        "title": "Average Authors in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_in_a_year(i)[1])
            for i in averages]})

    args['tables'] = tables
    return render_template("averages.html", args=args)


@app.route("/coauthors", methods=['GET', 'POST'])
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "coauthors"}
    args["title"] = "Co-Authors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4

    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)


@app.route("/", methods=['GET', 'POST'])
def showStatisticsMenu():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Publication Summary"
    args["data"] = db.get_publication_summary()
    return render_template('statistics.html', args=args)


@app.route("/statisticsdetails/<status>", methods=['GET', 'POST'])
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": status}

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    args["start_year"] = start_year
    args["end_year"] = end_year

    args["min_year"] = db.min_year
    args["max_year"] = db.max_year

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()

    args["status"] = status

    return render_template('statistics_details.html', args=args)

@app.route("/author_profile/<name>", methods=['GET', 'POST'])
def authorProfile(name):
    db = app.config['DATABASE']
    handled_name = replace(name, "%20", " ")
    args = {}
    args["title"] = handled_name
    args["data"] = db.get_author_statistics_detailed_all(handled_name)
    return render_template('statistics_details.html', args=args)

@app.route("/author_statistics", methods=['GET', 'POST'])
def showAuthorStatistics():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "author_statistics"}

    args["title"] = "Author Statistics"

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_author_statistics_with_sole(pub_type)
    args["pub_type"] = pub_type
    args["pub_str"] = PUB_TYPES[pub_type]

    return render_template('author_statistics.html', args=args)


@app.route("/network", methods=['GET', 'POST'])
def showPublicationNetwork():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "network"}

    # net = network.PublicationNetwork()
    # net.generateNetwork()

    args["title"] = "Publication Network"
    # args["data"] = "publication_network.png"

    return render_template('graph.html', args=args)


@app.route("/about", methods=['GET', 'POST'])
@login_required
def about():
    args = {}
    contact_form_handler(args)
    return render_template('about.html', args=args)


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(410)
@app.errorhandler(500)
def errorHandler(error):
    title = str(error)
    data = ""
    email = "dumbastic@gmail.com"
    if type(error) == exceptions.NotFound:
        title = "404"
        data = "Sorry, the page you are looking for may have been removed, deleted or it was never there! Maybe you should check the URL properly and try again. However, if you feel this is a fault on our side (or you just love to argue), report us at"
    elif type(error) == exceptions.Forbidden:
        title = "403"
        data = "Sorry, you dont have permission to access this page. Maybe you should log in first, or you just dont have the privilege to access this area. However, if you feel this is a fault on our side (or you just love to argue), report us at"
    elif type(error) == exceptions.MethodNotAllowed:
        title = "405"
        data = "Sorry, the method you are trying to invoke are not allowed. Maybe you should you should try to do whatever you want to do on a different page. However, if you feel this is a fault on our side (or you just love to argue), report us at"
    elif type(error) == exceptions.Gone:
        title = "410"
        data = "Sorry, the page you are looking for has been removed. You are out of luck. However, if you feel this is a fault on our side (or you just love to argue), report us at"
    elif type(error) == exceptions.InternalServerError:
        title = "500"
        data = "Oops, this time it is our fault. Something went wrong, and we will fix it. If this causes you fatal problem, report us at"
    request.path="/" #so if HTTP method POST are invoked (e.g login submit action) on error page, it will be redirected to index page instead
    args = {"title": title, "data": data, "email": email}
    return render_template('error.html', args=args)


def contact_form_handler(args):
    contactform = forms.ContactForm(prefix="contactform")
    args["contactform"] = contactform
    if request.method == 'POST':
        if 'contactform-submit' in request.form:
            if contactform.validate() == False:
                flash("All fields are required")
                args["contact_success"] = False
            else:
                msg = Message(contactform.subject.data, sender=contactform.email.data,
                              recipients=['dumbastic@gmail.com', 'cipherhat@gmail.com', 'ruvinbsu@gmail.com',
                                          'sylvain.huprelle@gmail.com'])
                msg.body = """
EMAIL GENERATED FROM JEFFRIES ABOUT PAGE. DO NOT REPLY TO THIS EMAIL. REPLY TO THE SENDER'S EMAIL ADDRESS CONTAINED INSIDE THIS EMAIL AS NECESSARY.

    From: %s <%s>
    %s
                """ % (contactform.name.data, contactform.email.data, contactform.message.data)
                mail.send(msg)
                args["contact_success"] = True


# the first method to be invoked before every page rendering - returning and handling login form
@app.context_processor
def login_form_handler():
    loginform = forms.LoginForm(prefix="loginform")
    def_dict = {'loginform':loginform}
    if request.method == 'POST' and "loginform-username" in request.form:
        if 'loginform-submit' in request.form:
            if loginform.validate() == False:
                flash("Login fail")
                def_dict["login_success"] = False
            else:
                username = request.form['loginform-username']
                password = request.form['loginform-password']
                print username, password
                registered_user = models.User.query.filter_by(username=username,password=password).first()
                if registered_user is None:
                    flash("Login fail")
                    def_dict["login_success"] = False
                else:
                    login_user(registered_user)
                    def_dict["login_success"] = True
    return dict(def_dict = def_dict)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    # user = User(request.form['username'] , request.form['password'],request.form['email'])
    # db.session.add(user)
    # db.session.commit()
    # flash('User successfully registered')
    # return redirect(url_for('login'))