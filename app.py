from flask import Flask, flash, render_template, redirect, g, url_for, request, session
import sqlite3
from UserPassword import UserPassword

### LOGIN AND PASSWORD OF THE ADMIN USER ###
### Login: 0d3Ug ###
### Password:admin ###

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

    if user_info.verify_correct:
        return redirect(url_for('index'))

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
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)
    
    if request.method == 'GET':
        return render_template('new_trip_form.html', active_menu='new_trip_idea', user_info=user_info)
    else:
        trip_name = '' if not 'trip_name' in request.form else request.form['trip_name']
        description = '' if not 'description' in request.form else request.form['description']
        completness = 'option2' if not 'completness' in request.form else request.form['completness']
        contact = False if not 'gridCheck1' in request.form else True

        if not trip_name or not description:
            flash('You must fill in the blanks')
            return render_template('new_trip_form.html', active_menu='new_trip_idea', user_info=user_info)

        sql_command = 'insert into trip_ideas (name, email, description, completness, contact, trip_author) values(?, ?, ?, ?, ?, ?);'
        db.execute(sql_command, [trip_name, user_info.email, description, completness, contact, user_info.name])
        db.commit()

        flash('You added new trip idea!')
        return redirect(url_for('index'))

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
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if user_info.is_admin and user_info.verify_correct:
        sql_command = 'select name, email, is_admin from users;'
        cursor = db.execute(sql_command)
        users_record = cursor.fetchall()

        return render_template('users.html', active_menu='users', users=users_record, user_info=user_info)
        
    else:
        return redirect(url_for('login'))

@app.route('/delete_user/<user_name>')
def delete_user(user_name):
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if not user_info.verify_correct or not user_info.is_admin:
        return redirect(url_for('login'))
    
    sql_command = 'delete from users where name=? and name <> ?;'
    db.execute(sql_command, [user_name, user_info.name])
    db.commit()

    if user_name == user_info.name:
        flash('Cannot delete a user')
    else:
        flash("User {} has been deleted".format(user_name))
    return redirect(url_for('users'))

@app.route('/edit_user_by_admin/<user_name>', methods=['GET', 'POST'])
def edit_user_by_admin(user_name):
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if not user_info.is_admin or not user_info.verify_correct:
        return redirect(url_for('login'))
    
    sql_command = 'select name, email from users where name=?;'
    cursor = db.execute(sql_command, [user_name])
    user_record = cursor.fetchone()

    if user_record == None:
        flash('No such user')
        return redirect(url_for('users'))


    if request.method == 'GET':
        return render_template('edit_user_by_admin.html', active_menu='users', user_info=user_info, user=user_record)   
    else:
        new_email = '' if not 'email' in request.form else request.form['email']
        new_password = '' if not 'user_pass' in request.form else request.form['user_pass'] 

        if new_email != user_record['email']:
            sql_command = 'select count(*) as cnt from users where email=?'
            cursor = db.execute(sql_command, [new_email])
            check_email_unique = cursor.fetchone()

            if check_email_unique['cnt'] == 0:
                sql_command = 'update users set email = ? where name = ?'
                db.execute(sql_command, [new_email, user_name])
                db.commit()
                flash('Email was updated successfully')
            else:
                flash('User with the email {} alresdy exists'.format(new_email))
                return render_template('edit_user_by_admin.html', active_menu='users', user_info=user_info, user=user_record)

        if new_password:
            user_pass = UserPassword(user_name, new_password)
            sql_command = 'update users set password = ? where name = ?;'
            db.execute(sql_command, [user_pass.hash_password(), user_name])
            db.commit()
            flash('Password was updated successfully')

        return redirect(url_for('users'))

@app.route('/edit_user_status/<user_name>')
def edit_user_status(user_name):
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if not user_info.is_admin or not user_info.verify_correct:
        return redirect(url_for('login'))

    if user_name == user_info.name:
        flash('You cannot change your status')
        return redirect(url_for('users'))
    
    sql_command = 'update users set is_admin=(is_admin + 1)%2 where name=?;' 
    db.execute(sql_command, [user_name])
    db.commit()
    
    flash("{}'s user status has changed".format(user_name))
    return redirect(url_for('users'))

@app.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    db = get_db()
    user_info = UserPassword(session.get('user'))
    user_info.get_user_info(db)

    if not user_info.verify_correct or user_info.is_admin:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('edit_account.html', active_menu='edit_account', user_info=user_info)
    else:
        new_email = '' if not 'email' in request.form else request.form['email']
        old_password = '' if not 'user_old_pass' in request.form else request.form['user_old_pass']
        new_password = '' if not 'user_pass' in request.form else request.form['user_pass']
        confirm_password = '' if not 'user_pass_confirm' in request.form else request.form['user_pass_confirm'] 

        if new_email != user_info.email:
            sql_command = 'select count (*) as cnt from users where email=?;'
            cursor = db.execute(sql_command, [new_email])
            check_email_unique = cursor.fetchone()

            if check_email_unique['cnt'] == 0:
                sql_command = 'update users set email=? where name=?;'
                db.execute(sql_command, [new_email, user_info.name])
                db.commit()
                flash('Email was updated successfully')
            else:
                flash('User with the email {} alresdy exists'.format(new_email))
                return render_template('edit_account.html', active_menu='edit_account', user_info=user_info)

        if old_password:
            user_info.password = old_password
            if user_info.verify_password(db):
                if new_password and new_password == confirm_password:
                    print("new_pass")
                    user_pass = UserPassword(user_info.name, new_password)
                    sql_command = 'update users set password=? where name=?;' 
                    db.execute(sql_command, [user_pass.hash_password(), user_info.name])
                    db.commit()
                    flash('Password was updated successfully')
                elif new_password != confirm_password:
                    flash('New password and Confirm password must be the same')
                    return render_template('edit_account.html', active_menu='edit_account', user_info=user_info)
            else:
                flash('The old password is incorrect')
                return render_template('edit_account.html', active_menu='edit_account', user_info=user_info)
        elif new_password:
            flash('You have to enter the old password')
            return render_template('edit_account.html', active_menu='edit_account', user_info=user_info)
            
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)