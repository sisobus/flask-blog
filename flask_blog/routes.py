#!/usr/bin/python
#-*- coding:utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

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
