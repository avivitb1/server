from flask import Blueprint, render_template

assignment_4 = Blueprint('assignment_4', _name_,
                         static_folder='static',
                         template_folder='templates')



@assignment_4.route('/assignment_4')
def assignment_4_func():
    return render_template('assignment_4.html')