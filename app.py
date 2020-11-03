from flask import Flask, request, jsonify, render_template, json, session
from ml_algorithm import algorithm
from random import randrange
import csv
from datetime import date
import os.path
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    username = session.get('username')
    if username:
        return render_template('index.html', userName="Welcome " + username)
    else:
        return render_template('index.html', signIn="sign in", singUp="sign up")

@app.route('/detect',methods=['POST'])
def detect():
    username = session.get('username')
    str_input = request.form.get('content')
    # if len(str_input)!=0:
    #     write_in(str_input,"unknown")
    res = algorithm.detect_spam(str_input)
    confScore = randrange(100)
    time = get_date()
    # write user, content, label, date, score to database
    label = "sus_benign"
    if res:
        label = "sus_spam"

    if 'detect' in request.form:
        if username:
            write_for_user(username, str_input, label, time, confScore)
        else:
            write_in(str_input,label)
        if res:
            return render_template('index.html', isSpam='Spam Warning!!!'+" Confidence Score: "+ str(confScore),userName="Welcome " + username)
        else:
            return render_template('index.html', notSpam='Safe! Not A Spam!' + " Confidence Score: "+ str(confScore), userName="Welcome " + username)
    elif 'report' in request.form:
        if username:
            write_for_user(username, str_input, "con_spam", time, 100)
        else:
            write_in(str_input,"con_spam")
        return render_template('index.html', getReport='Report Received! Thank you!', userName="Welcome " + username)

# nav jump
@app.route('/why_page')
def toWhyPage():
    username = session.get('username')
    if username:
        return render_template('why_page.html', userName = "Welcome " + username)
    else:
        return render_template('why_page.html', signIn = "sign in", singUp = "sign up")

@app.route('/service_page')
def toServicePage():
    username = session.get('username')
    if username:
        return render_template('service_page.html', userName="Welcome " + username)
    else:
        return render_template('service_page.html', signIn="sign in", singUp="sign up")

@app.route('/support_page')
def toSupportPage():
    username = session.get('username')
    if username:
        return render_template('support_page.html', userName="Welcome " + username)
    else:
        return render_template('support_page.html', signIn="sign in", singUp="sign up")

@app.route('/dash_board')
def toDashBoard():
    username = session.get('username')
    if username:
        return render_template('dash_board.html', userName="Welcome " + username)
    else:
        return render_template('dash_board.html')

@app.route('/sign_in')
def toSignIn():
    return render_template('sign_in.html')

@app.route('/sign_up')
def toSignUp():
    return render_template('sign_up.html')

# sign up
@app.route('/sign_in',methods=['POST'] )
def hasSignedUp():
    # get form data
    userName = request.form.get('userName')
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    pswConfirm = request.form.get('pswConfirm')
    print(userName, emailInput, pswInput,pswConfirm)

    if pswConfirm == pswInput:
        # write to database
        user_info_list = [userName,emailInput,pswInput]
        write_user_to_temp_database(user_info_list)
        # jump to sign in page
        return render_template('sign_in.html', allow ="Thank you for signing up. You can log in now")

# sign in
@app.route('/dash_board',methods=['POST'] )
def hasSignedIn():
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    userInfo = find_user_in_temp_database(emailInput, pswInput)
    if len(userInfo) == 0:
        return render_template('sign_in.html', warning ="User Not Found!" )

    session['username'] = userInfo[0]
    session.permanent = True
    return render_template('dash_board.html', userName = "Welcome " +userInfo[0])

# extension sign in
@app.route('/extension_sign',methods=['POST'])
def extensionSign():
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    print(emailInput, pswInput)
    userInfo = find_user_in_temp_database(emailInput, pswInput)
    if len(userInfo) == 0:
        return {"result":False}
    else:
        return {"result":userInfo}

def write_user_to_temp_database(user_info_list):
    with open("tempDatabase/users.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info_list)

def find_user_in_temp_database(emailInput, pswInput):
    with open("tempDatabase/users.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        userInfo = []
        for line in reader:
            if (emailInput == line[1]) and (pswInput == line[2]):
                userInfo = line
                return userInfo
        return userInfo

def write_in(str , label):
    with open("temp.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [str,label]
        writer.writerow(row)

def convert_to_json():
    csv_file = csv.DictReader(open('temp.csv', 'r'))
    json_list = []
    for row in csv_file:
        json_list.append(row)
    return json_list

def append_in_list(list,dest):
    with open(dest, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list)

def write_new_in_list(list,dest):
    tag_list = ["Twitter Content","Label","Date","Confidence Score"]
    with open(dest, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(tag_list)
        wr.writerow(list)

def write_for_user(user,content, label, date, score):
    file_name = "tempDatabase/"+user+".csv"
    list = [content,label,date,score];
    if os.path.exists(file_name):
        append_in_list(list,file_name)
    else:
        write_new_in_list(list, file_name)

def get_date():
    today = date.today()
    return today.strftime("%m/%d/%y")

@app.route('/detect_api/get_all', methods=['GET'])
def api_get():
    contents = convert_to_json()
    return jsonify(contents)

# report spam using post
@app.route('/detect_api/post_report',methods=['POST'])
def api_post_report():
    data = request.data.decode('utf-8')
    print(data)
    data_json = json.loads(data)
    #write data into user
    #write user, content, label, date, score to database
    username = data_json.get('user')
    str_input = data_json['tweet']
    time = get_date()
    label = "con_spam"
    # if we can get user
    if username:
        write_for_user(username,str_input,label,time,100)
    #or
    else:
        #write to public temp database
        write_in(str_input,label)
    return jsonify(data_json)

# detect spam using post
@app.route('/detect_api/post_detect',methods=['POST'])
def api_post_detect():
    data = request.data.decode('utf-8')
    print(data)
    data_json = json.loads(data)
    username = data_json.get('user')
    str_input = data_json['tweet']
    confScore = randrange(100)
    time = get_date()
    label = "sus_benign"
    if algorithm.detect_spam(str_input):
        result ="This is a spam!!!"
        print(result)
        label = "sus_spam"
    else:
        result = "Safe! Not a spam"
        print(result)
    # if we can get user
    if username:
        write_for_user(username, str_input, label, time, confScore)
    # or
    else:
        # write to public temp database
        write_in(str_input,label)
    return {'result': result,'score':confScore}
    # return jsonify(data_json)

@app.route('/detect_api/message')
def api_message():
    language = request.args.get('language')
    print(language)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)