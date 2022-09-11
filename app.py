from flask import Flask, flash, render_template, redirect, g
import sqlite3

app = Flask(__name__)
# secret key is needed to correct work of flashed messages
app.secret_key = 'secret_key'

# database connection
app.info = {'db_file':'C:/Users/Krzysiu/Desktop/Python/Python_Flask/Trip_udea_form_exercise_vol_2/data/tripdb.db'}

def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app.info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
        return g.sqlite_db

@app.teardown_appcontext
def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

        

@app.route('/app_init')
def app_init():
    return 'not implemented'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return 'not implemented'

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