from flask import Flask, flash

app = Flask(__name__)


@app.route('/app_init')
def app_init():
    return 'not implemented'

@app.route('/')
def index():
    return 'not implemented'

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