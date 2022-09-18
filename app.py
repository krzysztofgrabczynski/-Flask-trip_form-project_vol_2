from flask import Flask, flash, render_template, redirect, g, url_for
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
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return 'not implemented'

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