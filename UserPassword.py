import random, string, hashlib, binascii


class UserPassword():
    def __init__(self, name='', password=''):
        self.name = name
        self.password = password

    def hash_password(self):
        """Has a password for storing."""
        # the value generated using os.random(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04" 
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),
        salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password 

    @classmethod
    def get_random_name_and_password(self):
        random_name = ''.join(random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) for i in range(5))
        random_password = ''.join(random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) for i in range(5))

        return UserPassword(random_name, random_password)

    def verify_login(self, db):
        sql_command = 'select name, email, password, is_admin from users where name=?;'
        cursor = db.execute(sql_command, [self.name])
        user_record = cursor.fetchone()

        if user_record != None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

