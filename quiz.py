#import Config as Config
from flask import Flask,render_template,request,redirect,url_for
import pymysql
import boto3
from botocore.client import Config

hostname = 'myrds.cbajl5dcthzk.us-east-1.rds.amazonaws.com'
username = 'saipriya'
password = 'password'
database = 'JMeter'
myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, local_infile=True)
print "connect"
s3 = boto3.resource(
    's3',
    aws_access_key_id='AKIAJRDYO54L4JNMEZ3Q',
    aws_secret_access_key='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',
    config=Config(signature_version='s3v4'))
print "Hello"
app = Flask(__name__)

lists = []
@app.route('/')
def index():
    print "Hello"
    #return render_template('main.html')
    return render_template('upload.html')

@app.route('/list',methods=['get','post'])
def list():
    aa = {
        'username':'qwe',
        'fileName' : 'addg',
        'image' : 'tatatatat'
    }

    ab = {
        'username':'qwertyuiop',
        'fileName' : 'asdfghj',
        'image' : 'zxcvbn'
    }

    lists.append(aa)
    lists.append(ab)
    cur = myConnection.cursor()
    query1 = 'select photo_id,filename,img,comment from Photo'
    cur.execute(query1)
    img = cur.fetchall()

    print img
    print img[0].get('img')
    myConnection.commit()
    # url = img[2].get('img')
    return render_template('list.html', img = img)


@app.route('/comment',methods=['get','post'])
def comment():
    item = request.form['imgID']
    print "Item:"+item[1]
    # id = item[2]
    pic=item.get('photo_id')
    print pic
    cur = myConnection.cursor()
    addcomment = request.form['commenthere']
    #qq = "select comment from Photo where photo_id= " + item[0]
    qq="select comment from Photo where photo_id= " + pic
    print qq
    cur.execute(qq)
    comm = cur.fetchall()
    comnt = comm[0].get('comment')
    print comnt
    #comn2 = str(comnt) + str(addcomment)
    query = "update Photo set comment = concat('" + str(comnt) + " : ','" + str(addcomment) + "') where photo_id= " + item[0]
    print query
    cur.execute(query)
    myConnection.commit()
    #return "Comment added successfully"
    return render_template('comments.html', item=item)


@app.route('/addComment',methods=['get','post'])
def addComment():
    addcomment = request.form['add Comment']
    mycur = myConnection.cursor()
    query2 = 'update Photo set comment=concat(comment, %s) where photo_id=1' % (addcomment)
    print query2
    mycur.execute(query2)
    result = mycur.fetchall()
    print result
    query3='select comment from Photo where photo_id=1'
    mycur.execute(query3)
    result1 = mycur.fetchall()

    print result1
    myConnection.commit()
    # item = request.form['imgID']
    # print item
    # insertQuery = "insert into comments values('{{item.fileName'}},addcomment)"
    # cur.execute(insertQuery)
    # myConnection.commit()
    #return render_template('comments.html',res=result1)
    return "Comment added successfully"


@app.route('/upload',methods=['get','post'])
def upload():
    #global username
    # image_file = request.files['upload_files']
    # file_name = image_file.filename
    # print file_name
    # target = image_file.read()
    # comm = request.form['comments']
    # #fs = gridfs.GridFS(client.nmdb)
    # #fs.put(target, filename=file_name, user=username, comment=comm)
    # #insert into imageTable values('')
    return render_template('upload.html')

@app.route('/uploadImage',methods=['get','post'])
def upload1():
    f = request.files['upload_files']
    imgfile=request.form['file']
    file_name = f.filename
    comm = request.form['comments']
    file_content = f.read()
    s3.Bucket('saipriya').put_object(Key=file_name, Body=file_content, ACL='public-read')
    imgUrl = 'https://s3.amazonaws.com/saipriya/'+file_name
    #print imgUrl
    #insertQuery = "insert into Photo values ('"+file_name+"','"+comm+"','"+imgUrl+"')"
    insertQuery="insert into Photo (comment,filename,img) values ('%s','%s','%s')"%(comm,imgfile,imgUrl)
    print insertQuery
    cur = myConnection.cursor()
    cur.execute(insertQuery)
    print insertQuery
    query1 = 'select filename,img from Photo'
    cur.execute(query1)
    myConnection.commit()
    return "file uploaded"


@app.route('/login', methods=['POST'])
def login():
    return 'Invalid username/password combination'

@app.route('/query',methods=['get','post'])
def query():
    cur = myConnection.cursor()
    text = request.form['val1']
    #query2 = "Select count(*) from course where Course>%s" % text
    query2 = "Select * from course where Course>%s" % text
    cur.execute(query2)
    res = cur.fetchall()
    c = 0
    str1 = " "
    for row in res:
        c = c + 1
        str1 += str(c) + ':' + str(row) + '\n\n'
    return render_template('query.html', res=str1)

@app.route('/query1',methods=['get','post'])
def query1():
    cur = myConnection.cursor()
    text = request.form['val1']
    #query2 = "Select count(*) from course where Course>%s" % text
    query2 = "Select * from course where Course>%s" % text
    cur.execute(query2)
    res = cur.fetchall()
    c = 0
    str1 = " "
    for row in res:
        c = c + 1
        str1 += str(c) + ':' + str(row) + '\n\n'
    return render_template('query.html', res=str1)

@app.route('/query2',methods=['get','post'])
def query2():
    cur = myConnection.cursor()
    text = request.form['val1']
    #query2 = "Select count(*) from course where Course>%s" % text
    query2 = "Select * from course where Course>%s" % text
    cur.execute(query2)
    res = cur.fetchall()
    c = 0
    str1 = " "
    for row in res:
        c = c + 1
        str1 += str(c) + ':' + str(row) + '\n\n'
    return render_template('query.html', res=str1)

if __name__ == '__main__':
    app.run(debug=True)