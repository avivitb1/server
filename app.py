from flask import Flask, redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session, jsonify
from datetime import timedelta
app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/contact')
def Contact_func():
    return render_template('contact.html')

@app.route('/homepage')
def HomePage_func():
    return render_template('homepage.html')

@app.route('/assignment3_1')
def assignment3_1_func():  # put application's code here

    want_a_recipe = True
    user_name = 'aviv'
    food_names = {'name': 'sushi',  'country': 'china', 'time': '2 h '}
    food_types = ['Asian', 'Israeli', 'Italian', 'Poland', 'Arabic', 'American', 'Modern']
    return render_template('assignment3_1.html', want_a_recipe=want_a_recipe , user_name= user_name , food_names=food_names, food_types =food_types )

@app.route('/')
def default():
    name = "chf"
    if name == "":
        return redirect("/homepage")
    else:
        return redirect(url_for('assignment3_1_func'))

users=[{'name': 'Aviv', 'last_name': 'Hayun','email': 'aviv@gmail.com' , 'password': '123'},
       {'name': 'Eden', 'last_name': ' Levy','email': 'ed@gmail.com' , 'password': '759'},
       {'name': 'Gal', 'last_name': ' Swisa', 'email': 'gal@gmail.com', 'password': '292'},
       {'name': 'Liat', 'last_name': ' Hayun', 'email': 'liat@gmail.com', 'password': '647'},
       {'name': 'Tomer', 'last_name': ' Hacohen', 'email': 'tomer@gmail.com', 'password': '282'} ]


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_func():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
        user=next((item for item in users if item['name'] == user_name), None)

        if request.args['user_name'] == "":
            return render_template('assignment3_2.html',
                                   users=users)
        if user in users:
           return render_template('assignment3_2.html',
                                   user_name=user_name,
                                   user=user)
        else:
            return render_template('assignment3_2.html',
                                    message='user not found')

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = next((item for item in users if item['name'] == user_name), None)
        if user in users:
            user_password = user['password']
            if user_password == password:
                session['user_name'] = user_name
                session['logedin'] = True
                return render_template('assignment3_2.html',
                                       message2='Success Logged-in, ' + user_name,
                                       username=user_name)
            else:
                return render_template('assignment3_2.html',
                                       message2='Wrong password!')
        else:
            return render_template('assignment3_2.html',
                                    message2='The user dose not exist, Please sign in!')
    return render_template('assignment3_2.html')

@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('assignment3_2_func'))

if __name__ == '_main_':
    app.run(debug=True)