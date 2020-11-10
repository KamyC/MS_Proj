from flask import Flask, request, jsonify, render_template, json, session,redirect, url_for
from ml_algorithm import algorithm
from random import randrange
import tools.util
import tools.database
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    username = session.get('username')
    if username:
        # print("we get name")
        return render_template('index.html', userName="Welcome " + username)
    else:
        return render_template('index.html', signIn="Sign in", singUp="Sign up")

@app.route('/exit')
def logOut():
    print("remove user name")
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/detect',methods=['POST'])
def detect():
    username = session.get('username')
    str_input = request.form.get('content')
    res = algorithm.detect_spam(str_input)
    confScore = randrange(100)
    time = tools.util.get_date()
    # write user, content, label, date, score to database
    label = "sus_benign"
    if res:
        label = "sus_spam"
    if 'detect' in request.form:
        if username:
            tools.database.write_for_user(username, str_input, label, time, confScore)
        else:
            tools.database.write_in(str_input,label)
        if res:
            return render_template('index.html', isSpam='Spam Warning!!!'+" Confidence Score: "+ str(confScore),userName="Welcome " + username)
        else:
            return render_template('index.html', notSpam='Safe! Not A Spam!' + " Confidence Score: "+ str(confScore), userName="Welcome " + username)
    elif 'report' in request.form:
        if username:
            tools.database.write_for_user(username, str_input, "con_spam", time, 100)
        else:
            tools.database.write_in(str_input,"con_spam")
        return render_template('index.html', getReport='Report Received! Thank you!', userName="Welcome " + username)

# nav jump
@app.route('/why_page')
def toWhyPage():
    username = session.get('username')
    if username:
        return render_template('why_page.html', userName = "Welcome " + username)
    else:
        return render_template('why_page.html', signIn = "Sign in", singUp = "Sign up")

@app.route('/service_page')
def toServicePage():
    username = session.get('username')
    if username:
        return render_template('service_page.html', userName="Welcome " + username)
    else:
        return render_template('service_page.html', signIn="Sign in", singUp="Sign up")

@app.route('/support_page')
def toSupportPage():
    username = session.get('username')
    if username:
        return render_template('support_page.html', userName="Welcome " + username)
    else:
        return render_template('support_page.html', signIn="Sign in", singUp="Sign up")

@app.route('/dash_board')
def toDashBoard():
    username = session.get('username')
    if username:
        return render_template('dash_board.html', userName="Welcome " + username)
    else:
        return redirect(url_for('toSignIn'))

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
        tools.database.write_user_to_temp_database(user_info_list)
        # jump to sign in page
        return render_template('sign_in.html', allow ="Thank you for signing up. You can log in now")

# sign in
@app.route('/dash_board',methods=['POST'] )
def hasSignedIn():
    emailInput = request.form.get('emailInput')
    pswInput = request.form.get('pswInput')
    userInfo = tools.database.find_user_in_temp_database(emailInput, pswInput)
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
    userInfo = tools.database.find_user_in_temp_database(emailInput, pswInput)
    if len(userInfo) == 0:
        return {"result":False}
    else:
        return {"result":userInfo}

@app.route('/detect_api/get_all', methods=['GET'])
def api_get():
    contents = tools.util.convert_to_json()
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
    time = tools.util.get_date()
    label = "con_spam"
    # if we can get user
    if username:
        tools.database.write_for_user(username,str_input,label,time,100)
    #or
    else:
        #write to public temp database
        tools.database.write_in(str_input,label)
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
    time = tools.util.get_date()
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
        tools.database.write_for_user(username, str_input, label, time, confScore)
    # or
    else:
        # write to public temp database
        tools.database.write_in(str_input,label)
    return {'result': result,'score':confScore}
    # return jsonify(data_json)

@app.route('/detect_api/message')
def api_message():
    language = request.args.get('language')
    print(language)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)