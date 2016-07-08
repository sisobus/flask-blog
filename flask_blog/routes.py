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
import datetime
import os
import commands
import glob

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

"""
: blog util function
"""

def createDirectory(directoryName):
    if not os.path.exists(directoryName):
        command = 'mkdir %s'%directoryName
        ret = commands.getoutput(command)
        command = 'chmod 777 %s'%directoryName
        ret = commands.getoutput(command)


def get_max_post_number(filenames):
    ret = 0
    for filename in filenames:
        only_filename = filename.split('/')[-1] 
        only_number = int(only_filename.split('.')[0])
        ret = max(ret, only_number)
    return ret

def get_all_posts():
    createDirectory('/var/www/flask_blog/flask_blog/post/')
    filenames = glob.glob('/var/www/flask_blog/flask_blog/post/*.post')
    return filenames

def get_all_tags():
    with open('/var/www/flask_blog/flask_blog/post/tag','r') as fp:
        lines = fp.read().strip().split('\n')
    d = {}
    for line in lines:
        tag = line.split()[0]
        post_id = str(line.split()[1])
        if post_id in d:
            d[post_id].append(tag)
        else :
            d[post_id] = [tag]
    return d

def get_all_post_information(post_names):
    tags = get_all_tags()
    ret = []
    for post_name in post_names:
        d = {}
        with open(post_name,'r') as fp:
            lines = fp.read().strip().split('\n')
        post_id = post_name.split('/')[-1].split('.')[0]
        d['post_id'] = post_id
        d['post_name'] = lines[0]
        d['post_author'] = lines[1]
        d['post_date'] = lines[2]
        d['post_body'] = ''
        for body in lines[3:]:
            d['post_body'] += body+'\n'
        if post_id in tags:
            d['post_tags'] = tags[post_id]
        else:
            d['post_tags'] = []
        ret.append(d)
    ret = sorted(ret, key=lambda k: int(k['post_id']), reverse=True)
    return ret

"""
: blog route
"""
@app.route('/')
def main():
    posts = get_all_posts()
    ret_posts = get_all_post_information(posts)
    return render_template('blog.html',ret_posts=ret_posts)

@app.route('/create_post')
def create_post():
    posts = get_all_posts()
    ret_posts = get_all_post_information(posts)
    return render_template('create_post.html',ret_posts=ret_posts)


@app.route('/save_post',methods=['POST'])
def save_post():
    if request.method == 'POST':
        post_name = request.form['post_name']
        post_author = request.form['post_author']
        post_body = request.form['post_body']
        post_date = datetime.datetime.now()
        s = '%s\n%s\n%s\n%s'%(post_name,post_author,str(post_date),post_body)
        print post_name, post_author, post_body, post_date
        post_names = get_all_posts()
        last_post_number = get_max_post_number(post_names)
        post_id = last_post_number+1
        next_filename = '/var/www/flask_blog/flask_blog/post/%d.post'%(post_id)
        with open(next_filename,'w') as fp:
            fp.write(s)
        post_tags = request.form['tags'].split('#')
        if not os.path.exists('/var/www/flask_blog/flask_blog/post/tag'):
            commands.getoutput('touch /var/www/flask_blog/flask_blog/post/tag')
        with open('/var/www/flask_blog/flask_blog/post/tag','a') as fp:
            for post_tag in post_tags:
                cur_tag = post_tag.strip()
                if len(cur_tag) == 0:
                    continue
                fp.write(cur_tag+' '+str(post_id)+'\n')
        return redirect(url_for('main'))

@app.route('/post/<post_id>')
def post_detail(post_id):
    posts = get_all_posts()
    ret_posts = get_all_post_information(posts)
    ret = {}
    for post in ret_posts:
        if post['post_id'].strip() == post_id.strip():
            ret = post
    return render_template('post.html',ret_posts=ret_posts,post=ret)

if __name__ == '__main__':
    app.run(host='172.31.11.102',debug=True)
