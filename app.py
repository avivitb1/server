from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template

app = Flask(__name__)

@app.route('/contact')
def Contact_func():
    return render_template('contact.html')

@app.route('/homepage')
def HomePage_func():  # put application's code here
    return render_template('homepage.html')

@app.route('/assignment3_1')
def assignment3_1_func():  # put application's code here
    want_a_recipe = True
    user_name = 'aviv'
    food_names = {'name': 'sushi',  'shushi': 'Lilo', 'time': '2 h '}
    food_types = ['Asian', 'Italian', 'Israeli', 'Poland', 'Arabic', 'Marocan', 'Modern']
    return render_template('assignment3_1.html', want_a_recipe=want_a_recipe , user_name= user_name , food_names=food_names, food_types =food_types )

@app.route('/<name>')
def Page(name):
    if name == 'contact':
        return redirect(url_for('Contact_func'))


    if name == 'homepage':
        return redirect(url_for('HomePage_func'))

    # add if for assignment3_1

if __name__ == '__main__':
    app.run(debug=True)
