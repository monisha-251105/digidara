from flask import Flask,render_template,request,redirect 
from flask_mysqldb import MySQL
complaint=Flask(__name__)
complaint.config['MYSQL__HOST']='localhost'
complaint.config['MYSQL__PASSWORD']='yourpassword'
complaint.config['MYSQL__DB']='complaint_db'

mysql=MySQL(complaint)

@complaint.route('/submit',methods=['GET','POST'])
def submit_complaint():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        category=request.form['category']
        title=request.form['title']
        description=request.form['description']

        cur=mysql.connection.cursor()
        cur.execute('''
           INSERT INTO complaints(student_name,email,category,title,description)VALUES(%s,%s,%s,%s,%s)''',(name,email,category,title,description))
        mysql.connection.commit()
        return redirect(f'/my_complaints?email={email}')
    return render_template('submit_complaint.html')       

@complaint.route('/my_complaints')
def my_complaints():
    email=request.args.get('email')
    cur=mysql.connection.cursor()
    cur.execute("SELECT*FROM complaints WHERE email=%s ORDER BY submitted_on DESC",(email))
    complaints=cur.fetchall()
    return render_template('my_complaints.html',complaints=complaints,email=email)       

@complaint.route('/admin',methods=['GET','POST'])
def admin_view():
    if request.method=='POST':
        complaint_id=request.form['complaint_id']
        status=request.form['status']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE complaints SET status=%s WHERE complaint_id=%s",(status,complaint_id))
        mysql.connection.commit()
        
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM complaints ORDER BY submitted_on DESC")
    all_complaints=cur.fetchall()
    return render_template('admin_complaints.html',complaints=all_complaints) 

if (__name__)=='__main__' :
    complaint.run()  


                                            