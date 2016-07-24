# belt exam


# query = " INSERT INTO course (courses_name, Description, Date_added) VALUES (:course_name, :description, NOW())"
#         data = {
#             'course_name': details['course_name'],
#             'description': details['description']
#             }
#         return self.db.query_db(query,data)
# SELECT * FROM Customers
# ORDER BY Country limit 5
from system.core.model import Model
import re

class Loginmodel(Model):
    def __init__(self):
        super(Loginmodel, self).__init__()
    
    def create(self,data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not data['name']:
            errors.append('Name cannot be blank')
        elif len(data['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif data['password'] != data['confirm_password']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = data['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO user (name, alias, email, password) VALUES (:name, :alias, :email, :pw_hash)"
            details = {
                'name': data['name'],
                'alias': data['alias'],
                'email': data['email'],
                'pw_hash': hashed_pw
                }
            self.db.query_db(query,details)
            get_user_query = "SELECT * FROM user ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return {"status": True, "user": user[0]}

    
    def check_login(self,data):
        password = data['password']
        user_query = "SELECT * FROM user WHERE email = :email LIMIT 1"
        user_data = {'email': data['email']
                    }
        user = self.db.query_db(user_query, user_data)
        if not user:
            return False
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return {"user": user[0]}
            else:
                return False

    def quote_info(self, data):
        query = "SELECT quoted_by, quotes, user.name, user.id, quotes.id as quote_id FROM quotes LEFT JOIN user ON quotes.user_id = user.id"
        quotes_info =self.db.query_db(query)
        fav_query = "SELECT quotes.id as quote_id, quotes, quoted_by, user.name from favorites join quotes on quotes.id = favorites.quotes_id join user on quotes.user_id = user.id where favorites.user_id = :id group by quotes.id"
        fav_info = self.db.query_db(fav_query,data)
        return { 'all_info': quotes_info, 'fav_info': fav_info }

    def user_info(self, data):
        query = "SELECT quotes, quoted_by, user.name, count(*) as count from quotes left join user on quotes.user_id = user.id where user.id = :id group by user.id"
        users_info = self.db.query_db(query, data)
        return { 'user_display' : users_info}

    def quote(self, data):
        query = "INSERT INTO quotes (quotes, quoted_by, user_id) VALUES (:quote, :message, :id)"
        return self.db.query_db(query, data)

    def fav_info(self, data):
        query = "INSERT INTO favorites(user_id, quotes_id) VALUES (:user_id, :quote_id )"
        fab_info = self.db.query_db(query, data)
        return fab_info

    def remove(self, data):
        query = "DELETE FROM favorites WHERE user_id = :user_id and quotes_id = :quote_id"
        delete_info = self.db.query_db(query, data)
        return delete_info





















    