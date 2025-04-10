from flask import Flask,render_template,redirect,url_for,session,jsonify,flash  # type: ignore
from flask import request  # type: ignore
import random
from flaskext.mysql import MySQL # type: ignore
from flask_paginate import Pagination, get_page_parameter,get_page_args 
from datetime import date
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
app = Flask(__name__)
app.secret_key= "Super Secret key"
mysql = MySQL(app) 
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] =''
app.config['MYSQL_DATABASE_DB'] = 'project'
mysql.init_app(app)
@app.route('/')
def form():
    # conn = mysql.connect()
    # cursor =conn.cursor()
    # cursor.execute("select * from departments")
    # data=cursor.fetchall()
    # conn.commit()
    # conn.close()
    return render_template('main.html')
 
@app.route('/preg')
def preg():
    return render_template('registration.html')

@app.route('/reg',methods=['POST','GET'])
def reg():
  if request.method=='POST':
    id=''
    fname = request.form['fname']
    lname = request.form['lname']
    dob=request.form['dob']
    num=request.form['num']
    email=request.form['email']
    crpw=request.form['password']
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("INSERT INTO patientreg VALUES(%s,%s,%s,%s,%s,%s,%s)",(id,fname,lname,dob,num,email,crpw))
    conn.commit()
    conn.close()
    return redirect(url_for("login"))
    
@app.route('/dreg')
def dreg():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("select * from departments")
    data=cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template('doctorreg.html',data=data)

@app.route('/drreg',methods=['POST','GET'])
def drreg():
  if request.method=='POST':
    id=''
    fname = request.form['fname']
    lname = request.form['lname']
    dob=request.form['dob']
    num=request.form['num']
    special=request.form['dept_name']
    city=request.form['city']
    fees=request.form['fees']
    fromtime=request.form['time1']
    totime=request.form['time2']
    email=request.form['email']
    crpw=request.form['password']
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("INSERT INTO doctorreg VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,fname,lname,dob,num,special,city,fees,fromtime,totime,email,crpw))
    conn.commit()
    conn.close()
    return redirect (url_for("list"))
  
@app.route('/login')
def login():
    return render_template('loginn.html')

@app.route('/patient/login',methods=['POST','GET'])
def loginn():
    if request.method=='POST':
     email=request.form['email']
     crpw=request.form['password']
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("select * from patientreg where  email=%s and password=%s",(email,crpw))
     data=cursor.fetchone()
     if data:
        session['loggedin']=True
        session['username']=data[5]
        session['fname']=data[1]
        return redirect(url_for('patientin'))
     else:
        msg=' Incorrect Username/Password.Try Again!'
    return render_template('loginn.html',msg=msg)
@app.route('/patient/dashboard')
def patientin():
   return render_template('patientin.html',fname=session['fname'])

@app.route('/drlogin')
def drlogin():
    return render_template('dlogin.html')

@app.route('/dlogin',methods=['POST','GET'])
def dlogin():
    if request.method=='POST':
     email=request.form['email']
     crpw=request.form['password']
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("select * from doctorreg where  email=%s and password=%s",(email,crpw))
     data=cursor.fetchone()
     if data:
        session['loggedin']=True
        session['username']=data[10]
        return redirect(url_for('form'))
     else:
        msg=' Incorrect Username/Password.Try Again!'
    return render_template('dlogin.html',msg=msg)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cont',methods=['POST','GET'])
def cont():
    if request.method=='POST':
     id=''
     fname = request.form['fname']
    lname = request.form['lname']
    num=request.form['num']
    email=request.form['email']
    msg=request.form['msg']
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("INSERT INTO contact VALUES(%s,%s,%s,%s,%s,%s)",(id,fname,lname,num,email,msg))
    conn.commit()
    conn.close()
    return '<h1>Your Messsage is sent succesfully!!</h1>'

@app.route('/list',methods=['GET','POST'])
def list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
  
    prev_page = page - 1
    next_page = page + 1
    limit=5
    offset = page*limit - limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from doctorreg order by fname""")
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from doctorreg order by  fname
                        limit %s offset %s""", (limit, offset))
    data = cursor.fetchall()

    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('doclist.html', pagination=pagination,offset=offset,page=page,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)

@app.route('/admin')
def admin():
    return render_template('adminlogin.html')



@app.route('/admin/dashboard/adminprofile',methods=['GET'])
def aprofile():
   username=session['username']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute("select * from users where username=%s",username)
   data=cursor.fetchone()
   conn.commit()
   return render_template("adminprofile.html",data=data)

@app.route('/admin/dashboard')
def admindash():
    return render_template("adminin.html",username=session['username'])

@app.route('/admin/dashboard/doctors')
def viewd():
   return render_template("doctors.html")

@app.route('/logout')
def adlogout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return redirect(url_for('admin'))
@app.route('/admin/dashboard/patients',methods=['GET','POST'])
def pdetails():
   
    page = request.args.get(get_page_parameter(), type=int, default=1)
  
    prev_page = page - 1
    next_page = page + 1
    limit=5
    offset = page*limit - limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from patientreg order by fname""")
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from patientreg order by  fname
                        limit %s offset %s""", (limit, offset))
    data = cursor.fetchall()

    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('patients.html', pagination=pagination,offset=offset,page=page,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)

@app.route('/admin/dashboard/patients/addpatient')
def addpatient():
   return render_template("addpatient.html")

@app.route('/pedit',methods=['GET'])
def pedit():
    data =''
    id = request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'select * from patientreg where id='+ id
    cursor.execute(query)
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template("pedit.html",data=data)

@app.route('/pdelete',methods=['GET'])
def pdelete():
    pid= request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'delete from patientreg where id='+ pid
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect (url_for("pdetails"))

@app.route('/pupdate',methods=['POST'])
def pupdate():
    id=request.form['id']
    fname = request.form['fname']
    lname = request.form['lname']
    dob=request.form['dob']
    num=request.form['num']
    email=request.form['email']
    crpw=request.form['password']
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''update patientreg set
                   fname=%s,lname=%s,dob=%s,num=%s,email=%s,password=%s where id=%s''',
                    (fname,lname,dob,num,email,crpw,id) )
    conn.commit()
    conn.close()
    return redirect(url_for("pdetails"))
    
@app.route('/admin/dashboard/messages')
def msg():
    page = request.args.get(get_page_parameter(), type=int, default=1)
  
    prev_page = page - 1
    next_page = page + 1
    limit=5
    offset = page*limit - limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from contact order by fname""")
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from contact order by  fname
                        limit %s offset %s""", (limit, offset))
    data = cursor.fetchall()

    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('Messages.html', pagination=pagination,offset=offset,page=page,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)
@app.route('/admin/dashboard/appointments')
def appointments():
    page = request.args.get(get_page_parameter(), type=int, default=1)
  
    prev_page = page - 1
    next_page = page + 1
    limit=10
    offset = page*limit-limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from appointments order by name""")
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from appointments order by  name
                        limit %s offset %s""", (limit, offset))
    data = cursor.fetchall()

    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('appointments.html', pagination=pagination,offset=offset,page=page,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)

@app.route('/addnewappointment')
def addnewappointment():
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute("SELECT * FROM departments ORDER BY dept_id")
    departments = cursor.fetchall()
    conn.commit()
    conn.close()
    today=date.today()
    return render_template('addnewappointment.html', departments=departments,today=today)


@app.route('/doc/<name>')
def doc(name):
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute("SELECT * FROM doctorreg WHERE speciality = %s", [name])
    data = cursor.fetchall()  
    abc = []
    for row in data:
        dataObj = {
                'id': row[0],
                'fname': row[1],
                'lname':row[2]
               }
        abc.append(dataObj)
    return jsonify({'departmentdoc' : abc})

@app.route('/fee/<fees>')
def fee(fees):
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute("SELECT * FROM doctorreg WHERE docid = %s", [fees])
    fee = cursor.fetchall()  
    abcd = []
    for row in fee:
        Obj = {'fees': row[7]}
        abcd.append(Obj)
    return jsonify({'feedoc' : abcd})

@app.route('/admin/appointmentdetails',methods=['POST','GET'])
def aaddnewappde():
    if request.method=='POST':
     id=''
     name=request.form['pname']
     phone=request.form['num']
     email=request.form['email']
     dep=request.form['dep']
     date=request.form['date']
     time=request.form['time']
     doctor=request.form['name']
     fees=request.form['fees']
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("INSERT INTO  appointments values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,phone,email,dep,date,time,doctor,fees))
     conn.commit()
     conn.close()
    return redirect(url_for('appointments'))
@app.route('/appointmentedit',methods=['GET'])
def appointmentedit():
    data =''
    id = request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'select * from appointments where id='+ id
    cursor.execute(query)
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template("apppedit.html",data=data)

# @app.route('/admin/dashboard/departments')
# def departments():
#     conn = mysql.connect()
#     cursor =conn.cursor()
#     cursor.execute('select * from departments')
#     data=cursor.fetchall()
#     conn.commit()
#     conn.close() 
#     return render_template("departments.html",data=data)
    

@app.route('/admin/dashboard/departments/adddepartment',methods=['POST','GET'])
def adddept():
    if request.method=='POST':
     dept_id=''
     dept_name=request.form['dept_name']
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("INSERT INTO departments VALUES(%s,%s)",(dept_id,dept_name))
     conn.commit()
     conn.close()
     flash("Department Added Succesfully")
    return redirect(url_for('pagination'))

@app.route('/depdelete',methods=['GET'])
def depdelete():
     dept_id= request.args.get('id')
     conn = mysql.connect()
     cursor =conn.cursor()
     query = 'delete from departments where dept_id='+ dept_id
     cursor.execute(query)
     conn.commit()
     conn.close()
     flash("Record Deleted Successfully !!")
     return redirect(url_for('pagination'))

@app.route('/depedit',methods=['GET'])
def depedit():
    dept_id = request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'select * from departments where dept_id='+ dept_id
    cursor.execute(query)
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template("depedit.html",data=data)

@app.route('/depupdate/',methods=['POST'])
def depupdate():
   id=request.form['id']
   dept_name=request.form['dept_name']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(' update departments set dept_name=%s where dept_id=%s',(dept_name,id))
   conn.commit()
   return redirect(url_for('pagination'))


@app.route('/adprofileupdate/',methods=['POST'])
def adprofileupdate():
   id=request.form['id']
   name=request.form['name']
   phone=request.form['num']
   email=request.form['email']
   password=request.form['password']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(' update users set username=%s,phone=%s,email=%s,password=%s where id=%s',(name,phone,email,password,id))
   conn.commit()
   flash("Profile Updated Successfully")
   return redirect(url_for('aprofile'))
@app.route('/dredit',methods=['GET'])
def dredit():
    data =''
    docid = request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'select * from doctorreg where docid='+ docid
    cursor.execute(query)
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template("edit.html",data=data)

@app.route('/drupdate',methods=['POST'])
def drupdate():   
   id=request.form['id']
   fname = request.form['fname']
   lname = request.form['lname']
   dob=request.form['dob']
   num=request.form['num']
   special=request.form['spcl']
   city=request.form['city']
   fees=request.form['fees']
   fromtime=request.form['time1']
   totime=request.form['time2']
   email=request.form['email']
   crpw=request.form['password']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute('''update doctorreg set
   fname=%s,lname=%s,dob=%s,phone=%s,speciality=%s,city=%s,fees=%s,fromtime=%s,totime=%s,email=%s,password=%s
   where docid=%s''',(fname,lname,dob,num,special,city,fees,fromtime,totime,email,crpw,id))
   conn.commit()
   return redirect(url_for('list'))

@app.route('/delete',methods=['GET'])
def delete():
    docid= request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'delete from doctorreg where docid='+ docid
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect (url_for("list"))

@app.route('/mdelete',methods=['GET'])
def mdelete():
    msg_id= request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'delete from contact where msg_id='+ msg_id
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect (url_for("msg"))


@app.route('/patient/dashboard/newappointment',methods=['GET'])
def newapp():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("select *from departments order by dept_name")
    departments=cursor.fetchall()
    conn.commit()
    conn.close()  
    today = date.today()
    print(today)
    return render_template("newappointment.html",departments=departments,username=session['username'],today=today)



@app.route('/patient/dashboard/docname/<name>')
def docname(name):
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute("SELECT * FROM doctorreg WHERE speciality = %s", [name])
    data = cursor.fetchall()  
    abc = []
    for row in data:
        dataObj = {
                'id': row[0],
                'fname': row[1],
                'lname':row[2]
               }
        abc.append(dataObj)
    return jsonify({'departmentdoc' : abc})

@app.route('/patient/dashboard/docfee/<fees>')
def docfee(fees):
    conn = mysql.connect()
    cursor =conn.cursor()
    result = cursor.execute("SELECT * FROM doctorreg WHERE docid = %s", [fees])
    fee = cursor.fetchall()  
    abcd = []
    for row in fee:
        Obj = {'fees': row[7]}
        abcd.append(Obj)
    return jsonify({'feedoc' : abcd})

@app.route('/patient/appointmentdetails',methods=['POST','GET'])
def appde():
    if request.method=='POST':
     id=''
     name=request.form['pname']
     phone=request.form['num']
     email=request.form['email']
     dep=request.form['dep']
     date=request.form['date']
     time=request.form['time']
     doctor=request.form['name']
     fees=request.form['fees']
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("INSERT INTO  appointments values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,phone,email,dep,date,time,doctor,fees))
     conn.commit()
     conn.close()
    return redirect(url_for('apphistory'))
@app.route('/patient/dashboard/profile')
def patientprofile():
   username=session['username']
   fname=session['fname']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute("select * from patientreg where email=%s and fname=%s",(username,fname))
   data=cursor.fetchone()
   conn.commit()
   return render_template("patientprofile.html",data=data)
@app.route('/patient/dashboard/appointmenthistory')
def apphistory():
    username=session['username']
    fname=session['fname']
    page = request.args.get(get_page_parameter(), type=int, default=1) 
    prev_page = page - 1
    next_page = page + 1
    limit=10
    offset = page*limit - limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from appointments where email=%s """,(username))
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from appointments where email=%s 
                        limit %s offset %s""", (username,limit,offset))
    data = cursor.fetchall()
    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('apphistory.html', pagination=pagination,offset=offset,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)

@app.route('/pprofileupdate/',methods=['POST'])
def pprofileupdate():
   id=request.form['id']
   name=request.form['name']
   dob=request.form['dob']
   phone=request.form['num']
   email=request.form['email']
   password=request.form['password']
   conn = mysql.connect()
   cursor =conn.cursor()
   cursor.execute(" update patientreg set fname='{}',dob='{}',num='{}',email='{}',password='{}' where id='{}'".format(name,dob,phone,email,password,id))
   conn.commit()
   conn.close()
   flash("Profile Updated Successfully")
   return redirect(url_for('patientprofile'))

@app.route('/appdelete',methods=['GET'])
def appdelete():
    id= request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'delete from appointments where id='+ id
    cursor.execute(query)
    conn.commit()
    conn.close()    
    return redirect (url_for("apphistory"))

@app.route('/adminappdelete',methods=['GET'])
def adappdelete():
    id= request.args.get('id')
    conn = mysql.connect()
    cursor =conn.cursor()
    query = 'delete from appointments where id='+ id
    cursor.execute(query)
    conn.commit()
    conn.close()
    msg= " Appointment Deleted Successfully"
    return redirect (url_for("appointments",msg=msg))
@app.route('/admin/login',methods=['POST'])
def adminlogin():
     uname=request.form['uname']
     crpw=request.form['password']
     utype=1
     conn = mysql.connect()
     cursor =conn.cursor()
     cursor.execute("select * from users where username=%s and password=%s and user_type=%s",(uname,crpw,utype))
     data=cursor.fetchone()
     if data:
        session['loggedin']=True
        session['username']=data[1]
        flash("You are successfuly logged in")
        return redirect(url_for('admindash'))
     else:
        msg=' Incorrect Username/Password.Try Again!'
     return render_template('adminlogin.html',msg=msg)

@app.route('/searchdoc',methods=["POST","GET"])
def searchdoc():
   conn = mysql.connect()
   cursor =conn.cursor()
   if request.method=='POST':
      word=request.form['query']
      print(word)
      if word == '':
            query = "SELECT * from doctorreg ORDER BY docid"
            cursor.execute(query)
            data = cursor.fetchall()
      else:    
            query = "SELECT * from doctorreg WHERE fname LIKE '%{}%' OR lname LIKE '%{}%' OR speciality LIKE '%{}%' OR city LIKE '%{}%' ORDER BY docid DESC LIMIT 20".format(word,word,word,word)
            cursor.execute(query)
            numrows = int(cursor.rowcount)
            data = cursor.fetchall()
            print(numrows)
      return jsonify({'htmlresponse': render_template('z8.html', data=data, numrows=numrows)})
   


@app.route('/admin/dashboard/departments')
def pagination():  
    page = request.args.get(get_page_parameter(), type=int, default=1) 
    prev_page = (page - 1)
    next_page = page + 1
    limit=5
    offset = page*limit - limit
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""select * from departments order by dept_name""")
    result = cursor.fetchall()
    total = len(result)
    cursor.execute("""select * from departments order by  dept_name
                        limit %s offset %s""", (limit, offset))
    data = cursor.fetchall()
    pagination = Pagination(page=page, page_per=limit, total=total)
    return render_template('departments.html',result=result, pagination=pagination,offset=offset,page=page,limit=limit, data = data, next_page=next_page, prev_page=prev_page,total=total)
    

@app.route('/abc')
def index():
    return render_template('chatbot.html')

def hospital_chatbot(user_message):
    if "appointment" in user_message:
        response = "You can schedule an appointment by clicking on the 'Schedule Appointment' button."
    elif "doctor" in user_message:
        response = "You can find a list of our doctors on the 'Doctors' page."
    elif "services" in user_message:
        response = "We offer a wide range of services, including diagnostics, surgery, and emergency care."
    else:
        response = "I'm sorry, I couldn't understand your request. How can I assist you further?"
    return response
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        response = hospital_chatbot(user_message)
        return jsonify({"message": response})
    else:
        return jsonify({"message": "Please provide a message."})

if __name__=='__main__':
    app.run(debug=True)
