from flask import Flask, render_template, request, session
import mysql.connector
from werkzeug.utils import secure_filename
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static'
app.secret_key = 'maharazu'


english_bot = ChatBot("iStudBot", logic_adapters=[
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.<br> Kindly ask '
                            'questions regarding International Student Visa',
        'maximum_similarity_threshold': 0.50
    }
], storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    if session.get('loggedin'):
        vid = session['uname']
        return render_template("index.html", user=vid)
    elif session.get('ploggedin'):

        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


@app.route("/dashboard")
def dashboard():
    vid = session['uname']
    return render_template("options.html", user=vid)


@app.route("/logout")
def logout():
    session['loggedin'] = False
    session['ploggedin'] = False
    return "<script>alert('You been logged out.');</script>" + home()


@app.route("/plogout")
def plogout():
    session['ploggedin'] = False
    session['loggedin'] = False
    return "<script>alert('You been logged out.');</script>" + home()


@app.route("/about")
def about():
    if session.get('loggedin'):
        vid = session['uname']
        return render_template("about.html", user=vid)
    elif session.get('ploggedin'):
        # vid = session['uname']
        return render_template("about.html")
    else:
        return render_template("about.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/iputralog")
def iputralog():
    return render_template("iputralog.html")


@app.route("/chat")
def chat():
    return render_template("chatbotfloat.html")


@app.route("/optionp")
def optionp():
    vid = session['uname']
    return render_template("options.html", user=vid)


@app.route("/applyp")
def applyp():
    vid = session['uname']
    return render_template("apply.html", user=vid)


@app.route("/newstud")
def newstud():
    vid = session['uname']
    return render_template("newstudent.html", user=vid)


@app.route("/depend")
def depend():
    vid = session['uname']
    return render_template("dependant.html", user=vid)


@app.route("/viewrenewal")
def viewrenewal():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM renewal")
    data = mycursor.fetchall()
    return render_template("viewren.html", data=data)


@app.route("/viewnewstud")
def viewnewstud():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM newstudent")
    data = mycursor.fetchall()
    return render_template("viewnew.html", data=data)


@app.route("/viewdepend")
def viewdepend():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dependant")
    data = mycursor.fetchall()
    return render_template("viewdepend.html", data=data)


@app.route('/viewappdetail/<id>/<type>')
def viewappdetail(id,type):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    vid = id
    vtype = type
    mycursor = mydb.cursor()
    if type=='depend':
        mycursor.execute("SELECT * FROM dependant WHERE id='" + vid + "'")
        data = mycursor.fetchall()
        return render_template('viewappdetail.html', data=data, type=type)
    elif type=='new':
        mycursor.execute("SELECT * FROM newstudent WHERE id='" + vid + "'")
        data = mycursor.fetchall()
        return render_template('viewappdetail.html', data=data, type=type)
    else:
        mycursor.execute("SELECT * FROM renewal WHERE id='" + vid + "'")
        data = mycursor.fetchall()
        return render_template('viewappdetail.html', data=data, type=type)


@app.route('/notif/<type>')
def notif(type):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    vid = session['matric']
    user = session['uname']
    mycursor = mydb.cursor()
    cursor = mydb.cursor()

    mycursor.execute("SELECT * FROM notif")
    data = mycursor.fetchall()
    for row in data:
        if type == "new":
            cursor.execute("SELECT newstudent.id, newstudent.matric, notif.type, newstudent.remark, notif.remark "
                           "FROM notif, newstudent WHERE newstudent.id=notif.vid AND newstudent.matric='" + vid + "'"
                           "AND notif.type='" + type + "'")
            datas = cursor.fetchall()
            return render_template('notifications.html', data=datas, user=user, type=type)
        elif type == "depend":
            cursor.execute("SELECT dependant.id, dependant.matric, notif.type, dependant.remark, notif.remark FROM "
                           "notif,dependant WHERE dependant.id=notif.vid AND dependant.matric='" + vid + "'"
                           "AND notif.type='" + type + "'")
            datas = cursor.fetchall()
            return render_template('notifications.html', data=datas, user=user, type=type)
        else:
            cursor.execute("SELECT renewal.id, renewal.matric, notif.type, renewal.remark, notif.remark "
                           "FROM notif, renewal WHERE renewal.id=notif.vid AND renewal.matric='" + vid + "'"
                           "AND notif.type='" + type + "'")
            datas = cursor.fetchall()
            return render_template('notifications.html', data=datas, user=user, type=type)


@app.route('/remarkdecline/<id>/<type>')
def remarkdecline(id,type):
    return render_template('decline.html', data=id, type=type)


@app.route('/approve/<id>/<type>')
def approve(id,type):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    vid = id
    vtype = type
    mycursor = mydb.cursor()
    if type == "depend":
        mycursor.execute("INSERT INTO notif(vid,type,remark) VALUE(" + id + ",'" + type + "','All details accepted')")
        mycursor.execute("UPDATE dependant SET remark='Approved' WHERE id='" + vid + "'")
        mydb.commit()
        mycursor.close()
        return '<script>alert("APPLICATION DOCUMENTS APPROVED!");</script>' + render_template('poptions.html')
    elif type == "new":
        mycursor.execute("INSERT INTO notif(vid,type,remark) VALUE(" + id + ",'" + type + "','All details accepted')")
        mycursor.execute("UPDATE newstudent SET remark='Approved' WHERE id='" + vid + "'")
        mydb.commit()
        mycursor.close()
        return '<script>alert("APPLICATION DOCUMENTS APPROVED!");</script>' + render_template('poptions.html')
    else:
        mycursor.execute("INSERT INTO notif(vid,type,remark) VALUE(" + id + ",'" + type + "','All details accepted')")
        mycursor.execute("UPDATE renewal SET remark='Approved' WHERE id='" + vid + "'")
        mydb.commit()
        mycursor.close()
        return '<script>alert("APPLICATION DOCUMENTS APPROVED!");</script>' + render_template('poptions.html')


@app.route('/decline', methods=['POST', 'GET'])
def decline():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        id = reg['vid']
        type = reg['type']
        remark = reg['remark']
        if type == "new":
            mycursor.execute("INSERT INTO notif(vid, type, remark) VALUES(%s, 'new', %s)",
                             (id, remark))
            mycursor.execute("UPDATE newstudent SET remark = 'Declined' WHERE id='" + id + "'")
            mydb.commit()
            mycursor.close()

            return '<script>alert("APPLICATION DOCUMENTS DECLINED!");</script>' + render_template('poptions.html')
        elif type == "depend":
            mycursor.execute("INSERT INTO notif(vid, type, remark) VALUES(%s, 'depend', %s)",
                             (id, remark))
            mycursor.execute("UPDATE dependant SET remark = 'Declined' WHERE id='" + id + "'")
            mydb.commit()
            mycursor.close()

            return '<script>alert("APPLICATION DOCUMENTS DECLINED!");</script>' + render_template('poptions.html')
        else:
            mycursor.execute("INSERT INTO notif(vid, type, remark) VALUES(%s, 'renewal', %s)",
                             (id, remark))
            mycursor.execute("UPDATE renewal SET remark = 'Declined' WHERE id='" + id + "'")
            mydb.commit()
            mycursor.close()

            return '<script>alert("APPLICATION DOCUMENTS DECLINED!");</script>' + render_template('poptions.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        matric = reg['matric']
        name = reg['name']
        passport = reg['passport']
        faculty = reg['faculty']
        password = reg['password']
        mycursor.execute("INSERT INTO registration(matric, name, passport, faculty, password) VALUES(%s,%s,%s,%s,%s)",
                         (matric, name, passport, faculty, password))
        mydb.commit()
        mycursor.close()
        session['loggedin'] = True
        session['matric'] = matric
        session['uname'] = name

        return render_template('options.html', user=name)


@app.route('/log', methods=['POST', 'GET'])
def log():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        matric = reg['matric']
        password = reg['password']
        mycursor.execute("SELECT * FROM registration WHERE matric=%s AND password=%s",
                         (matric, password))
        account = mycursor.fetchone()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['matric'] = account[0]
            session['password'] = account[4]
            session['uname'] = account[1]
            # Redirect to home page
            return "<script>alert('LOGIN SUCCESSFUL!');</script>" + render_template('options.html', user=account[1])
        else:
            # Account doesnt exist or username/password incorrect
            return "<script>alert('LOGIN FAILED!');</script>" + render_template('login.html')
        mydb.commit()
        mycursor.close()


@app.route('/iputralogin', methods=['POST', 'GET'])
def iputralogin():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        staffid = reg['staffid']
        password = reg['password']
        mycursor.execute("SELECT * FROM iputrastaff WHERE staffid=%s AND password=%s",
                         (staffid, password))
        account = mycursor.fetchone()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['ploggedin'] = True
            session['staffid'] = account[0]
            session['password'] = account[1]
            # Redirect to home page
            return "<script>alert('LOGIN SUCCESSFUL!');</script>" + render_template('poptions.html')
        else:
            # Account doesnt exist or username/password incorrect
            return "<script>alert('LOGIN FAILED!');</script>" + render_template('iputralog.html')
        mydb.commit()
        mycursor.close()


@app.route('/apply', methods=['POST', 'GET'])
def apply():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        matric = reg['matric']
        email = reg['email']
        phone = reg['phone']
        passport = reg['passport']
        photo = request.files['photo']
        photo.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(photo.filename)))
        passp = request.files['passp']
        passp.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(passp.filename)))
        offer = request.files['offer']
        offer.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(offer.filename)))
        med = request.files['med']
        med.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(med.filename)))
        acr = request.files['acadresult']
        acr.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(acr.filename)))
        atr = request.files['atreport']
        atr.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(atr.filename)))
        payment = request.files['payment']
        payment.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(payment.filename)))
        aform = request.files['aform']
        aform.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(aform.filename)))
        mycursor.execute("INSERT INTO renewal(matric, email, phone, passportno, photo, passup, regslip, medical, "
                         "acadresult, atreport, payment, aform) VALUES(%s,%s,%s,%s, "
                         "%s,%s,%s,%s,%s,%s,%s,%s)",
                         (matric, email, phone, passport, photo.filename, passp.filename, offer.filename, med.filename, acr.filename,atr.filename, payment.filename, aform.filename))
        mydb.commit()
        mycursor.close()
        vid = session['uname']

        return "<script>alert('APPLICATION SUBMITTED!');</script>" + render_template("apsuccess.html", user=vid)


@app.route('/applynew', methods=['POST', 'GET'])
def applynew():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        # type = 'New'
        matric = reg['matric']
        email = reg['email']
        phone = reg['phone']
        passport = reg['passport']
        photo = request.files['photo']
        photo.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(photo.filename)))
        passp = request.files['passp']
        passp.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(passp.filename)))
        offer = request.files['offer']
        offer.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(offer.filename)))
        med = request.files['med']
        med.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(med.filename)))
        val = request.files['val']
        val.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(val.filename)))
        payment = request.files['payment']
        payment.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(payment.filename)))
        aform = request.files['aform']
        aform.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(aform.filename)))
        mycursor.execute(
            "INSERT INTO newstudent(matric,email,phone,passportno,photo,passup,regslip,medical,val,payment,aform) VALUES(%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s)",
            (matric, email, phone, passport, photo.filename, passp.filename, offer.filename, med.filename, val.filename, payment.filename, aform.filename))
        mydb.commit()
        mycursor.close()
        vid = session['uname']

        return "<script>alert('APPLICATION SUBMITTED!');</script>" + render_template("apsuccess.html", user=vid)


@app.route('/applydepend', methods=['POST', 'GET'])
def applydepend():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iputra"
    )
    mycursor = mydb.cursor()
    if request.method == 'POST':
        reg = request.form
        type = 'Dependant'
        matric = reg['matric']
        email = reg['email']
        phone = reg['phone']
        passport = reg['passport']
        photo = request.files['photo']
        photo.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(photo.filename)))
        passp = request.files['passp']
        passp.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(passp.filename)))
        passd = request.files['passd']
        passd.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(passd.filename)))
        med = request.files['med']
        med.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(med.filename)))
        val = request.files['val']
        val.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(val.filename)))
        proof = request.files['offer']
        proof.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(proof.filename)))
        payment = request.files['payment']
        payment.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(payment.filename)))
        aform = request.files['aform']
        aform.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(aform.filename)))
        mycursor.execute(
            "INSERT INTO dependant(matric, email, phone, passportno, photo, passup, passd, medical, bankst, proof, "
            "payment, aform) VALUES(%s,%s,%s,%s,%s, "
            "%s,%s,%s,%s,%s,%s,%s)",
            (matric, email, phone, passport, photo.filename, passp.filename, passd.filename,med.filename, val.filename, proof.filename, payment.filename, aform.filename))
        mydb.commit()
        mycursor.close()
        vid = session['uname']

        return "<script>alert('APPLICATION SUBMITTED!');</script>" + render_template("apsuccess.html", user=vid)

if __name__ == "__main__":
    app.run(debug=True)
