from comp61542 import app, mail
from database import database
from visualization import network
from flask import (render_template, request, send_file)
from werkzeug import exceptions
from flask_mail import Message
from forms import forms

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([(fmt % i).rstrip('0').rstrip('.') for i in item]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result


@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "averages"}
    loginFormHandler(args)
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


@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "coauthors"}
    loginFormHandler(args)
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


@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    loginFormHandler(args)
    args["title"] = "Publication Summary"
    args["data"] = db.get_publication_summary()
    return render_template('statistics.html', args=args)


@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": status}
    loginFormHandler(args)

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
        args["data"] = db.get_publications_by_year(start_year, end_year)

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()

    if (status == "author_statistics"):
        args["title"] = "Author Statistics"
        args["data"] = db.get_author_statistics()

    args["status"] = status

    return render_template('statistics_details.html', args=args)


@app.route("/network")
def showPublicationNetwork():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "network"}
    loginFormHandler(args)

    # net = network.PublicationNetwork()
    # net.generateNetwork()

    args["title"] = "Publication Network"
    # args["data"] = "publication_network.png"

    return render_template('graph.html', args=args)


@app.route("/about", methods=['GET', 'POST'])
def aboutUs():
    args = {}
    loginFormHandler(args)
    contactFormHandler(args)
    return render_template('about.html', args=args)


@app.errorhandler(403)
@app.errorhandler(404)
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
    elif type(error) == exceptions.Gone:
        title = "410"
        data = "Sorry, the page you are looking for has been removed. You are out of luck. However, if you feel this is a fault on our side (or you just love to argue), report us at"
    elif type(error) == exceptions.InternalServerError:
        title = "500"
        data = "Oops, this time it is our fault. Something went wrong, and we will fix it. If this causes you fatal problem, report us at"

    args = {"title": title, "data": data, "email": email}
    loginFormHandler(args)
    return render_template('error.html', args=args)


def contactFormHandler(args):
    contactform = forms.ContactForm(prefix="contactform")
    args["contactform"] = contactform
    if request.method == 'POST':
        if 'contactform-submit' in request.form:
            if contactform.validate() == False:
                args["success"] = False
            else:
                msg = Message(contactform.subject.data, sender=contactform.email.data,
                              recipients=['dumbastic@gmail.com', 'cipherhat@gmail.com', 'ruvinbsu@gmail.com',
                                          'sylvain.huprelle@gmail.com'])
                msg.body = """
EMAIL GENERATED FROM JEFFRIES ABOUT PAGE. DO NOT REPLY TO THIS EMAIL. REPLY TO THE SENDER'S EMAIL
ADDRESS CONTAINED INSIDE THIS EMAIL AS NECESSARY.

    From: %s <%s>
    %s
                """ % (contactform.name.data, contactform.email.data, contactform.message.data)
                mail.send(msg)
                args["success"] = True


def loginFormHandler(args):
    loginform = forms.LoginForm(prefix="login")
    args["loginform"] = loginform

