from flask import Flask,render_template,request,redirect,session,flash
import mysql.connector as db_connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

connectionVariable=db_connector.connect(host='localhost',user='root',password='',database='adv_sadiq_database')

@app.route('/')
def login_func():
    if 'currentUser' in session:
        return redirect('/home')
    else:
        return render_template('login.html')

@app.route('/loginValidation',methods=['POST'])
def validation():
    username=request.form.get('name')
    userpassword=request.form.get('password')
    cursorVar=connectionVariable.cursor()
    cursorVar.execute("""select * from `admin` where `name` like '{}' and `password` like '{}'""".format(username,userpassword))
    adminData=cursorVar.fetchall()
    if len(adminData)>0:
        session['currentUser']=adminData[0][0]
        #if details match...session is created
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/home')
def home_func():
    if 'currentUser' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/createRecord')
def create_func():
    if 'currentUser' in session:
        return render_template('create.html')
    else:
        return redirect('/')

@app.route('/insertRecordToDB',methods=['POST'])
def insertRecordfunc():
    if 'currentUser' in session:
        appNo=request.form.get('appNo')
        date=request.form.get('date')
        trademark=request.form.get('trademark')
        classOfItem=request.form.get('class')
        name=request.form.get('name')
        tradingAs=request.form.get('tradingAs')
        address=request.form.get('address')
        mobileNo=request.form.get('mobile')
        govtFees=request.form.get('govtFees')
        advocateFees=request.form.get('advocateFees')
        paymentMode=request.form.get('paymentMode')
        chequeNumber=request.form.get('chequeNumber')
        bankName=request.form.get('bankName')
        status=request.form.get('status')
        remarks=request.form.get('remarks')
        
        cursor2=connectionVariable.cursor()
        cursor2.execute("""select * from `client_table` where `application_no` = '{}'""".format(appNo))
        #length non-zero hui to if execute hojayega
        if len(cursor2.fetchall()):
            return redirect('/recordAlreadyExist')
        else:
            cursor1=connectionVariable.cursor()
            cursor1.execute("""insert into `client_table`(`s_no`,`application_no`,`date_of_application`,`trademark`,`class`,`name_of_prop_partner_director`,`trading_as`,`address`,`mobile_no`,`govt_fees`,`advocate_fees`,`payment_mode`,`cheque_no`,`bank_name`,`net_status`,`remarks`) values(NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(appNo,date,trademark,classOfItem,name,tradingAs,address,mobileNo,govtFees,advocateFees,paymentMode,chequeNumber,bankName,status,remarks))
            connectionVariable.commit()
            return redirect('/successfulRecordInsertion')
    else:
        return redirect('/')

@app.route('/recordAlreadyExist')
def raeFunc():
    if 'currentUser' in session:
        return render_template('rae.html')
    else:
        return redirect('/')

@app.route('/successfulRecordInsertion')
def successInsert():
    if 'currentUser' in session:
        return render_template('successRegister.html')
    else:
        return redirect('/')

@app.route('/read')
def readFunc():
    if 'currentUser' in session:
        return render_template('read.html')
    else:
        return redirect('/')

@app.route('/readAll')
def readAllfunc():
    if 'currentUser' in session:
        readAllCursor=connectionVariable.cursor()
        readAllCursor.execute("""select * from `client_table`""")
        readAllVar=readAllCursor.fetchall()
        return render_template('read_all.html',readAllVar=readAllVar)
    else:
        return redirect('/')

@app.route('/recordOfClientUsingAppNo',methods=['POST'])
def readOneFunc():
    if 'currentUser' in session:
        clientAppNo=request.form.get('client_id')
        cursor4=connectionVariable.cursor()
        cursor4.execute("""select * from `client_table` where `application_no`='{}'""".format(clientAppNo))
        clientDetail=cursor4.fetchall()
        return render_template('read_all.html',readAllVar=clientDetail)
    else:
        return redirect('/')

@app.route('/recordOfClientUsingName',methods=['POST'])
def recUsingNameFunc():
    if 'currentUser' in session:
        clientName=request.form.get('client_name')
        cursor5=connectionVariable.cursor()
        cursor5.execute("""select * from `client_table` where `name_of_prop_partner_director` like '{}'""".format(clientName))
        userDetail=cursor5.fetchall()
        return render_template('read_all.html',readAllVar=userDetail)
    else:
        return redirect('/')

@app.route('/updatePage')
def updateFunc():
    if 'currentUser' in session:
        return render_template('update.html')
    else:
        return redirect('/')

@app.route('/searchAfterUpdate',methods=['POST'])
def sauFunc():
    if 'currentUser' in session:
        appNo=request.form.get('user_id')
        cursorVar=connectionVariable.cursor()
        cursorVar.execute("""select * from `client_table` where `application_no` ='{}'""".format(appNo))
        global extractUser
        extractUser=cursorVar.fetchall()
        return render_template('searchAfter.html',extractedUser=extractUser)
    else:
        return redirect('/')

@app.route('/finalUpdateAfterSearch',methods=['POST'])
def fuas_func():
    if 'currentUser' in session:
        appNo=request.form.get('appNo')
        date=request.form.get('date')
        trademark=request.form.get('trademark')
        classOfItem=request.form.get('class')
        name=request.form.get('name')
        tradingAs=request.form.get('tradingAs')
        address=request.form.get('address')
        mobileNo=request.form.get('mobile')
        govtFees=request.form.get('govtFees')
        advocateFees=request.form.get('advocateFees')
        paymentMode=request.form.get('paymentMode')
        chequeNumber=request.form.get('chequeNumber')
        bankName=request.form.get('bankName')
        status=request.form.get('status')
        remarks=request.form.get('remarks')
        oldApplicationNo=extractUser[0][1]
        cursorVar=connectionVariable.cursor()
        cursorVar.execute("""update `client_table` set `application_no`='{}' ,`date_of_application`='{}',`trademark`='{}',`class`='{}',`name_of_prop_partner_director`='{}',`trading_as`='{}',`address`='{}',`mobile_no`='{}',`govt_fees`='{}',`advocate_fees`='{}',`payment_mode`='{}',`cheque_no`='{}',`bank_name`='{}',`net_status`='{}',`remarks`='{}' where `application_no`='{}'""".format(appNo,date,trademark,classOfItem,name,tradingAs,address,mobileNo,govtFees,advocateFees,paymentMode,chequeNumber,bankName,status,remarks,oldApplicationNo))
        connectionVariable.commit()
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/deleteRecord')
def delete_func():
    if 'currentUser' in session:
        return render_template('delete.html')
    else:
        return redirect('/')

@app.route('/deleteUsingApplicationNo',methods=['POST'])
def delUsingAppNo():
    if 'currentUser' in session:
        user_id=request.form.get('id')
        cursor2=connectionVariable.cursor()
        cursor2.execute("""select * from `client_table` where `application_no`='{}'""".format(user_id))
        if len(cursor2.fetchall()):
            cursor3=connectionVariable.cursor()
            cursor3.execute("""delete from `client_table` where `application_no`='{}'""".format(user_id))
            connectionVariable.commit()
            return 'record deleted successfully'
        else:
            return render_template('delete.html')
    else:
        return redirect('/')

@app.route('/deleteUsingName',methods=['POST'])
def delUsingName():
    if 'currentUser' in session:
        user_name=request.form.get('userName')
        cursor1=connectionVariable.cursor()
        cursor1.execute("""select * from `client_table` where `name_of_prop_partner_director`='{}'""".format(user_name))
        #agr kuch detail isme aayi to hi delete krna hai
        if len(cursor1.fetchall()):
            cursor6=connectionVariable.cursor()
            cursor6.execute("""delete from `client_table` where `name_of_prop_partner_director`='{}'""".format(user_name))
            connectionVariable.commit()
            return 'record deleted successfully'
        else:
            return render_template('delete.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout_func():
    if 'currentUser' in session:
        session.pop('currentUser')
        flash('logged out successfully','success')
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)