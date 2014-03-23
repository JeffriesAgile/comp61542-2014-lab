__author__ = 'CipherHat'
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
from flask_mail import Mail, Message


class ContactForm(Form):
    name = TextField("Name", [validators.Required("Please enter your name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter a valid email address.")])
    subject = TextField("Subject", [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message", [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")


mail = Mail()


def initialise(app):
    mail.init_app(app)


def contactFormHandler(args, contactform):
    if contactform.validate() == False:
        args["success"] = False
    else:
        msg = Message(contactform.subject.data, sender=contactform.email.data,
                      recipients=['dumbastic@gmail.com', 'cipherhat@gmail.com', 'ruvinbsu@gmail.com',
                                  'sylvain.huprelle@gmail.com'])
        msg.body = """EMAIL GENERATED FROM JEFFRIES ABOUT PAGE. DO NOT REPLY TO THIS EMAIL. REPLY TO THE SENDER'S EMAIL
ADDRESS CONTAINED INSIDE THIS EMAIL AS NECESSARY.

    From: %s <%s>
    %s
        """ % (contactform.name.data, contactform.email.data, contactform.message.data)
        mail.send(msg)
        args["success"] = True

