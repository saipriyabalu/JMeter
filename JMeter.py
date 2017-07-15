import boto3,os
import pymysql  # connect to rds--mysql
import time  # query time
import memcache  # importing memcache
import hashlib  # for hashing the queries
from botocore.client import Config
from flask import Flask, request
from flask import render_template
import time

# credentials to connect to the database
hostname = 'myrds.cbajl5dcthzk.us-east-1.rds.amazonaws.com'
username = 'saipriya'
password = 'password'
database = 'JMeter'
myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database,charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, local_infile=True)
print "Connected to SQL"
cur = myConnection.cursor()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload',methods=['POST'])
def upload():
    f=request.files['file']
    c=request.form['comment']
    query= "INSERT INTO Photo (img,comment) VALUES('C:/Users/Saipriya/Desktop/%s','%s')" % (f,c)
    cur.execute(query)
    myConnection.commit()
    return "Image uploaded successfully"

@app.route('/query',methods=['POST'])
def query():
    starttime=time.time()
    getdata=request.form['val1']
    query="select count(*) from course where Course>%s"% getdata
    cur.execute(query)
    myConnection.commit()
    res=cur.fetchall()
    endtime=time.time()
    total=endtime-starttime
    return total+str(res)

@app.route('/update',methods=['POST'])
def update():
    Val1 = request.form['val1']
    Val2 = request.form['val2']
    Val3= request.form['val3']


    render_template('index.html')



if __name__ == '__main__':
    app.run()
