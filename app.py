# from asyncio import FastChildWatcher
from ast import If
from dataclasses import fields
from doctest import FAIL_FAST
from msilib import schema
from sqlite3 import SQLITE_ALTER_TABLE
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
import io 
import openpyxl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class QuestionTable(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    air = db.Column(db.Integer)
    neetrollno = db.Column(db.Integer)
    cetformno = db.Column(db.Integer)
    regsrno = db.Column(db.Integer)
    name = db.Column(db.String(30))
    g = db.Column(db.String(5))
    cat = db.Column(db.String(10))
    quota = db.Column(db.String(15))
    code = db.Column(db.Integer)
    college = db.Column(db.String(50))

    def __init__(self, sno, air, neetrollno, cetformno, regsrno, name, g, cat, quota, code, college):
        self.sno = sno
        self.air = air
        self.neetrollno = neetrollno
        self.cetformno = cetformno
        self.regsrno = regsrno
        self.name = name
        self.g = g
        self.cat = cat
        self.quota = quota
        self.code = code
        self.college = college

# class Postschema(ma.Schema):
#     class Meta:
#         fields = ( 'sno','air', 'neetrollno', 'cetformno', 'regsrno', 'name', 'g', 'cat', 'quota', 'code', 'college')

# post_schema = Postschema()
# posts_schema = Postschema(many=True)


@app.route('/upload', methods=['POST'])
def excelfile():
    if request.method=='POST':
        if request.files:
            uploaded_file = request.files['file']
            wb_obj=openpyxl.load_workbook(uploaded_file)
            page=wb_obj.active
            i=0
            for row in page.values:
                print(page.values)
                i +=1
                print(i)
                if i==1:
                    continue
                else:
                    posts=QuestionTable(*row)
                    db.session.add(posts)
                    db.session.commit()
            return jsonify({'msg' : 'uploaded'})

if __name__ == '__main__':
    app.run(debug=True)