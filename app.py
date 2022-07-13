from flask import Flask, redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session, jsonify
from datetime import timedelta
# from assignment_4.assignment_4 import assignment_4,users
import mysql.connector
import requests


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

if __name__ == '__main__':
    app.run(debug=True)

# app.register_blueprint(assignment_4)


@app.route('/assignment_4')
def assignment_4_func():
    return render_template('assignment_4.html')

def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='viva0507605043',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

@app.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    print(query)
    return render_template('assignment_4.html', users=users_list)

@app.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['user_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    print(f'{name} {last_name} {email} {password}')
    query = "INSERT INTO users(name, last_name, email, password) VALUES ('%s', '%s', '%s', '%s'); " % (name, last_name, email, password)
    interact_db(query=query, query_type='commit')
    return redirect('/users')

@app.route('/update_user', methods=['POST'])
def update_user_func():
        name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        query = "UPDATE users SET email = '%s' WHERE name='%s';" % (email, name)
        interact_db(query, query_type='commit')
        query = "UPDATE users SET password ='%s' WHERE name='%s';" % (password, name)
        interact_db(query, query_type='commit')
        return redirect('/users')


@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_name = request.form['user_name']
    query = "DELETE FROM users WHERE name='%s';" % user_name
    interact_db(query, query_type='commit')
    return redirect('/users')

def get_users_sync(from_val):
    array = []
    res = requests.get(f'https://reqres.in/api/users/{from_val}')
    array.append(res.json())
    print(array)
    return array

def save_users_to_session(array):
    users_list_to_save = []
    for user in array:
        user_dict = {}
        # user_dict['sprites'] = {}
        user_dict['sprites'] = user['data']['avatar']
        user_dict['first_name'] = user['data']['first_name']
        user_dict['last_name'] = user['data']['last_name']
        user_dict['email'] = user['data']['email']
        # print(user['data']['first_name'])
        users_list_to_save.append(user_dict)
    session['array'] = users_list_to_save

@app.route('/fetch')
def fetch_func():
    if 'type' in request.args:
        num = int(request.args['num'])
        session['num'] = num
        array = []

        if request.args['type'] == 'sync':
            array = get_users_sync(num)

        save_users_to_session(array)
        return render_template('fetch.html',
                               userss=array)
    else:
        session.clear()
        return render_template('fetch.html')

