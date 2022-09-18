from flask import Flask, flash, render_template, redirect, g, url_for, request, session
import sqlite3
from UserPassword import UserPassword

### LOGIN AND PASSWORD OF THE ADMIN USER ###
### Login: 0d3Ug ###
### Password:mimED ###

app = Flask(__name__)
# secret key is needed to correct work of flashed messages
app.secret_key = 'secret_key'

# database connection
app.info = {'db_file':'C:/Users/Krzysiu/Desktop/Python/Python_Flask/Flask-trip_form-project_vol_2/Flask-trip_form-project_vol_2/data/tripdb.db'}

def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app.info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
   

@app.route('/app_init')
def app_init():
    db = get_db()

    sql_command = "select count(*) as cnt from users where is_admin;"
    cursor = db.execute(sql_command)
    is_admin = cursor.fetchone()

    if is_admin['cnt'] < 1:
        new_admin = UserPassword.get_random_name_and_password()
        hash_password = new_admin.hash_password()

        sql_command = "insert into users (name, email, password, is_admin) values (?, ?, ?, ?);"
        db.execute(sql_command, [new_admin.name, 'admin@admin.com', hash_password, True])
        db.commit()

        flash("You just set new admin on this server! Login: {} and password: {}".format(new_admin.name, new_admin.password))
        return redirect(url_for('index'))

    else:
        flash("You already set up the server")
        return redirect(url_for('index'))


@app.route('/')
def index():
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    return render_template('index.html', user_info=user_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if request.method == 'GET':
        return render_template('login.html', active_menu='login', user_info=user_info)
    
    else:
        user_name = '' if not 'user_name' in request.form else request.form['user_name']
        user_pass = '' if not 'user_pass' in request.form else request.form['user_pass']

        user = UserPassword(user_name, user_pass)
        user_verify = user.verify_login(db)
        
        if user_verify != None:
            session['user'] = user_name
            flash('Login successful, welcome!')
            return redirect(url_for('index'))
        else:
            flash('Login failed, please try again')
            return render_template('login.html', active_menu='login', user_info=user_info)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('You are logged out')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    message = []

    if request.method == 'GET':
        return render_template('register.html', active_menu='login', user_info=user_info)
    else:
        user_name = '' if not 'user_name' in request.form else request.form['user_name']
        user_email = '' if not 'email' in request.form else request.form['email']
        user_password = '' if not 'user_pass' in request.form else request.form['user_pass']

        sql_command = 'select name from users where name=?;'
        cursor = db.execute(sql_command, [user_name])
        user_record = cursor.fetchone()
        is_user_name_unique = False if user_record != None else True

        sql_command = 'select email from users where email=?;'
        cursor = db.execute(sql_command, [user_email])
        user_record = cursor.fetchone()
        is_user_email_unique = False if user_record != None else True

        if user_name == '':
            message.append('name cannot be empty')
        if user_email == '':
            message.append('email cannot be empty')
        if user_password == '':
            message.append('password cannot be empty')
        if not is_user_name_unique:
            message.append('user with the name {} already exists'.format(user_name))
        if not is_user_email_unique:
            message.append('user with the email {} alresdy exists'.format(user_email))

        if not message:
            new_user = UserPassword(user_name, user_password)
            sql_command = 'insert into users (name, email, password, is_admin) values (?, ?, ?, ?);'
            db.execute(sql_command, [user_name, user_email, new_user.hash_password(), False])
            db.commit()
            
            flash('User {} was successfully created.'.format(user_name))
            return redirect(url_for('login'))

        else:
            flash('Failure while creating user: {}'.format(', '.join(message)))
            return render_template('register.html', active_menu='login', user_info=user_info)

@app.route('/new_trip_idea', methods=['GET', 'POST'])
def new_trip_idea():
    return 'not implemented'

@app.route('/history')
def history():
    return 'not implemented'

@app.route('/edit_trip_idea/<int:trip_idea_id>', methods=['GET', 'POST'])
def edit_trip_idea(trip_idea_id):
    return 'not implemented'

@app.route('/delete_trip_idea/<int:trip_idea_id>')
def delete_trip_idea(trip_idea_id):
    return 'not implemented'    

@app.route('/users')
def users():
    return 'not implemented'

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    return 'not implemented'

@app.route('/delete_user/<user_name>')
def delete_user(user_name):
    return 'not implemented'

@app.route('/edit_user/<user_name>', methods=['GET', 'POST'])
def edit_user(user_name):
    return 'not implemented'   


if __name__ == '__main__':
    app.run()