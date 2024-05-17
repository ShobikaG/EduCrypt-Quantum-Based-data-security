from flask import Flask, render_template, request, send_file, redirect, url_for,session,jsonify
from pymongo import MongoClient
from QKD import encrypt_data,e91_secure_data_transmission
from bson import ObjectId 

app = Flask(__name__,template_folder='templates', static_folder='static')

app.secret_key = 'User'
active_sessions = {}

client = MongoClient('mongodb://localhost:27017/')
db = client['EduCrypt']
students_collection = db['Students_record']
nontechnical_collection = db['Nontechnical']
users_collection= db['login']
db = client['EduCryptSecured']
student_collection = db['StudentDetails']
nontechnicalsecured_collection = db['Employee_data']

app.secret_key = 'EduCrypt@1234'
active_sessions = {}

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'] 
    if username=="admin" and password=="1234":
        return render_template('admin.html')       
    else:
        return render_template('index.html')

@app.route('/logout')
def logout():
    session_token = session.get('session_token')
    if session_token in active_sessions:
        del active_sessions[session_token]
    session.clear()
    return redirect(url_for('main'))

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/Addmission', methods=['POST'])
def Addmission():

    enroll = request.form.get('enroll')
    name = request.form.get('name')
    dob = request.form.get('dob')
    Register_no = request.form.get('rno')
    caste = request.form.get('caste')
    email = request.form.get('email')
    p_no = request.form.get('pno')
    fname = request.form.get('fname')
    fPno = request.form.get('fpno')
    add = request.form.get('add')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    pro = request.form.get('pro')
    year = request.form.get('year')
    aadhar=request.form.get('aadhar')
    y12 = request.form.get('y12')
    n12 = request.form.get('n12')
    no12 = request.form.get('no12')
    y10 = request.form.get('y10')
    n10 = request.form.get('n10')
    no10 = request.form.get('no10')

    num_qubits = 100
    data_key = e91_secure_data_transmission(num_qubits)
    na = encrypt_data(name, data_key)
    ca = encrypt_data(caste, data_key)
    em = encrypt_data(email, data_key)
    pno = encrypt_data(p_no,data_key)
    fpnoo=encrypt_data(fPno,data_key)
    address = encrypt_data(add,data_key)
    aad =encrypt_data(aadhar,data_key)
    noo12=encrypt_data(no12,data_key)
    noo10=encrypt_data(no10,data_key)

    student_collection.insert_one({
        'enroll': enroll,
        'name': na,
        'dob': dob,
        'Register_no': Register_no,
        'caste': ca,
        'email': em,
        'p_no': pno,
        'fname': fname,
        'fPno': fpnoo,
        'add': address,
        'city': city,
        'state': state,
        'zip': zip,
        'pro': pro,
        'year':year,
        'aadhar':aad,
        'y12': y12,
        'n12': n12,
        'no12': noo12,
        'y10': y10,
        'n10': n10,
        'no10': noo10
    })

 


    students_collection.insert_one({
        'enroll': enroll,
        'name': name,
        'dob': dob,
        'Register_no': Register_no,
        'caste': caste,
        'email': email,
        'p_no': p_no,
        'fname': fname,
        'fPno': fPno,
        'add': add,
        'city': city,
        'state': state,
        'zip': zip,
        'pro': pro,
        'year':year,
        'aadhar':aadhar,
        'y12': y12,
        'n12': n12,
        'no12': no12,
        'y10': y10,
        'n10': n10,
        'no10': no10
    })

    return render_template('admission.html',enroll=enroll)

@app.route('/studentrecord')
def studentrecord():
    students = list(students_collection.find())
    return render_template('studentrecord.html',students=students)

@app.route('/edit/<student_id>')
def edit(student_id):
    student = students_collection.find_one({'_id': ObjectId(student_id)})
    return render_template('admission_edit.html', student=student)

@app.route('/update/<student_id>', methods=['POST'])
def update(student_id): 
    enroll = request.form.get('enroll')
    name = request.form.get('name')
    dob = request.form.get('dob')
    Register_no = request.form.get('rno')
    caste = request.form.get('caste')
    email = request.form.get('email')
    p_no = request.form.get('pno')
    fname = request.form.get('fname')
    fPno = request.form.get('fpno')
    add = request.form.get('add')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    pro = request.form.get('pro')
    year = request.form.get('year')
    aadhar=request.form.get('aadhar')
    y12 = request.form.get('y12')
    n12 = request.form.get('n12')
    no12 = request.form.get('no12')
    y10 = request.form.get('y10')
    n10 = request.form.get('n10')
    no10 = request.form.get('no10')
    
    students_collection.update_one({'_id': ObjectId(student_id)}, {'$set': {
        'enroll': enroll,
        'name': name,
        'dob': dob,
        'Register_no': Register_no,
        'caste': caste,
        'email': email,
        'p_no': p_no,
        'fname': fname,
        'fPno': fPno,
        'add': add,
        'city': city,
        'state': state,
        'zip': zip,
        'pro': pro,
        'year':year,
        'aadhar':aadhar,
        'y12': y12,
        'n12': n12,
        'no12': no12,
        'y10': y10,
        'n10': n10,
        'no10': no10
    }})
    students = list(students_collection.find())
    return render_template('studentrecord.html',enroll=enroll,students=students)



@app.route('/delete/<student_id>')
def delete(student_id):
    students_collection.delete_one({'_id': ObjectId(student_id)})
    students = list(students_collection.find())
    dele="Student record deleted successfully"
    return render_template('studentrecord.html',dele=dele,students=students)

@app.route('/nontechnical')
def nontechnical():
    nontechnical = list(nontechnical_collection.find())
    return render_template('nontechnical.html',nontechnical=nontechnical)


@app.route('/nontechnicaldetail', methods=['POST'])
def nontechnicaldetail():
    name = request.form.get('name')
    dob = request.form.get('dob')
    add = request.form.get('add')
    P_no = request.form.get('p_no')
    email = request.form.get('email')
    aadhar = request.form.get('aadhar')
    jobtitle = request.form.get('jt')
    dept = request.form.get('dept')
    sname = request.form.get('sname')
    sd = request.form.get('sd')
    es = request.form.get('es')
    el = request.form.get('el')
    num_qubits = 100
    data_key = e91_secure_data_transmission(num_qubits)
    na = encrypt_data(name, data_key)
    em = encrypt_data(email, data_key)
    pno = encrypt_data(P_no,data_key)
    address = encrypt_data(add,data_key)
    aad =encrypt_data(aadhar,data_key)

    nontechnicalsecured_collection.insert_one({
            'name': na,
            'dob': dob,
            'add': address,
            'p_no': pno,
            'email': em,
            'aadhar': aad,
            'jt': jobtitle,
            'dept': dept,
            'sname': sname,
            'sd': sd,
            'es': es,
            'el': el
    })

    nontechnical_collection.insert_one({
            'name': name,
            'dob': dob,
            'add': add,
            'p_no': P_no,
            'email': email,
            'aadhar': aadhar,
            'jt': jobtitle,
            'dept': dept,
            'sname': sname,
            'sd': sd,
            'es': es,
            'el': el
    })

    nontechnical = list(nontechnical_collection.find())
    return render_template('nontechnical.html',nontechnical=nontechnical,name=name)

@app.route('/delete/<nontechnical_id>')
def deletenon(nontechnical_id):
    nontechnical_collection.delete_one({'_id': ObjectId(nontechnical_id)})
    nontechnical = list(students_collection.find())
    dele="Employee record deleted successfully"
    return render_template('nontechnical.html',dele=dele,nontechnical=nontechnical)

@app.route('/management')
def management():
    return render_template('management.html')

@app.route('/Technical')
def technical():
    return render_template('technical.html')

if __name__ == '__main__':
    app.run(debug=True)
