#!/usr/bin/python
#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from config import (
        MAIL_SERVER,
        MAIL_PORT,
        MAIL_USE_TLS,
        MAIL_USE_SSL,
        MAIL_USERNAME,
        MAIL_PASSWORD
        )

app = Flask(__name__)

app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME 
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

from flask.ext.mail import Mail
mail = Mail(app)
from flask.ext.mail import Message
from decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app,msg)

@app.route('/2016-06-30')
def test_2016_06_30():
    return render_template('2016-06-30.html')

@app.route('/contact_mail',methods=['GET','POST'])
def contact_mail():
    if request.method == 'GET':
        return render_template('2016-06-30.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comments = request.form['comments']
        send_email(u'반갑습니다.',
                    MAIL_USERNAME,
                    [email],
                    u'반갑습니다. 바디입니다.',
                    u'반갑습니다. html입니다. %s님이 쓰신 %s는 잘 읽었습니다. 다만 들어줄 수 없습니다 .'%(name,comments))
        return redirect(url_for('test_2016_06_30'))

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/a')
def a():
    return render_template('a.html')

@app.route('/b')
def b():
    with open('visit','r') as fp:
        count = int(fp.read().strip())
    count += 1
    with open('visit','w') as fp:
        fp.write(str(count))
    return render_template('b.html',count=count)

if __name__ == '__main__':
    app.run(host='172.31.11.102',debug=True)
