from flask import Flask, redirect, Blueprint
from flask import url_for
from flask import render_template
from flask import request
from flask import session, jsonify
from datetime import timedelta
import mysql.connector
import requests

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/')
def default():
    name = "chf"
    if name == "":
        return redirect(url_for('assignment3_1_func'))
    else:
        return redirect("/homepage")

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


users=[{'first_name': 'Aviv', 'last_name': 'Hayun','email': 'aviv@gmail.com' , 'password': '123'},
       {'first_name': 'Eden', 'last_name': ' Levy','email': 'ed@gmail.com' , 'password': '759'},
       {'first_name': 'Gal', 'last_name': ' Swisa', 'email': 'gal@gmail.com', 'password': '292'},
       {'first_name': 'Liat', 'last_name': ' Hayun', 'email': 'liat@gmail.com', 'password': '647'},
       {'first_name': 'Tomer', 'last_name': ' Hacohen', 'email': 'tomer@gmail.com', 'password': '282'} ]


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_func():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
        user=next((item for item in users if item['user_name'] == user_name), None)

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

@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))

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
def users_func():
        query = 'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return render_template('users.html', users=users_list)

@app.route('/insert_user', methods=['POST'])
def insert_user():
    #id_name = request.form['id']
    name = request.form['name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    print(f'{name} {last_name} {email} {password}')
    query = "INSERT INTO users(name, last_name, email, password) VALUES ('%s','%s', '%s', '%s')" % (name, last_name, email, password)
    interact_db(query=query, query_type='commit')
    return redirect('/users')

@app.route('/update_user', methods=['POST'])
def update_user_func():
    # id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    query = "UPDATE users SET email ='%s' WHERE name='%s';" % (email, name)
    interact_db(query, query_type='commit')
    query = "UPDATE users SET name ='%s' WHERE name='%s';" % (name, name)
    interact_db(query, query_type='commit')
    query = "UPDATE users SET password ='%s' WHERE name='%s';" % (password, name)
    interact_db(query, query_type='commit')
    return redirect('/users')

@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    name = request.form['name']
    query = "DELETE FROM users WHERE name='%s';" % name
    # print(query)
    interact_db(query, query_type='commit')
    return redirect('/users')

#---------------------------------------#
#---------part b------------------------#
#---------------------------------------#

@app.route('/fetch_fe')
def fetch_func():
    return render_template('fetch_frontend.html')

def get_users_sync(from_val):
    pockemons = []
    res = requests.get(f'https://reqres.in/api/users/{from_val}')
    pockemons.append(res.json())
    print(pockemons)
    return pockemons

def save_users_to_session(pockemons):
    users_list_to_save = []
    for user in pockemons:
        user_dict = {}
        # user_dict['sprites'] = {}
        user_dict['sprites'] = user['data']['avatar']
        user_dict['first_name'] = user['data']['first_name']
        user_dict['last_name'] = user['data']['last_name']
        user_dict['email'] = user['data']['email']
        # print(user['data']['first_name'])
        users_list_to_save.append(user_dict)
    session['pockemons'] = users_list_to_save

@app.route('/assignment4/backend')
def fetch_be_func():
    if 'type' in request.args:
        print('type')
        num = int(request.args['num'])
        session['num'] = num
        pockemons = []

        if request.args['type'] == 'sync':
            pockemons = get_users_sync(num)
        save_users_to_session(pockemons)
        return render_template('fetch.html')

    else:
        session.clear()
        return render_template('fetch.html')

@app.route('/get_json')
def json_func():
    sample_dic = {
        'name': 'Yossi',
        'age': 25,
        'hobbies': ['swimming', 'art', 'sports']
    }
    return jsonify(sample_dic)


@app.route('/assignment4/restapi_users', defaults={'USER_ID': 1})
@app.route('/assignment4/restapi_users/<int:USER_ID>')
def get_user_by_ID(USER_ID):
    query = f'select * from users where id ={USER_ID}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': 'user not found'
        }
    else:
        user_list=users_list[0]
        return_dict = {
            'name': user_list.name,
            'last_name': user_list.last_name,
            'email': user_list.email
        }
#
# @app.route('/profile', defaults={'user_id': -1})
# @app.route('/profile/<int:user_id>')
# def profile_func(user_id):
#     # DB
#     response = {}
#
#     if user_id == -1:
#         response['message'] = 'No user inserted'
#
#     else:
#
#         query = "SELECT * FROM users WHERE id='%s';" % user_id
#         query_result = interact_db(query=query, query_type='fetch')
#         if len(query_result) != 0:
#             response = query_result[0]
#
#     response = jsonify(response)
#     return response

#
# @app.route('/get_users', defaults={'user_id': -1})
# @app.route('/get_users/<user_id>')
# def get_user(user_id):
#     if user_id == -1:
#         query = f'select * from users'
#         users_list = interact_db(query, query_type='fetch')
#         return_list = []
#         for user in users_list:
#             user_dict = {
#                 'name': user.name,
#                 'email': user.email,
#                 'create_date': user.create_date
#             }
#             return_list.append(user_dict)
#         return jsonify(return_list)
#
#     query = f'select * from users where id={user_id}'
#     users_list = interact_db(query, query_type='fetch')
#
#     if len(users_list) == 0:
#         return_dict = {
#             'message': 'user not found'
#         }
#     else:
#         user_list = users_list[0]
#         return_dict = {
#             'name': user_list.name,
#             'email': user_list.email,
#             'create_date': user_list.create_date
#         }
#     return jsonify(return_dict)
if __name__ == '__main__':
    app.run(debug=True)
