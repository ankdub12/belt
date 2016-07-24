# belt exam

from system.core.controller import *

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Loginmodel')
        self.db = self._app.db
   
    def index(self):
        if session.has_key('id'):
            data = {
            'id': session['id']
            }
            display_data = self.models['Loginmodel'].quote_info(data)
            return self.load_view('mainpage.html', quote_info=display_data['all_info'], fav_info=display_data['fav_info'])       
        else:
            return self.load_view('index.html')

    def logout(self):
        if session.has_key('id'):
            session.pop('id')
        if session.has_key('name'):
            session.pop('name')
        return redirect('/')


    def create(self):
        data = {
        'name': request.form['name'],
        'alias': request.form['alias'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
        }
        create_status = self.models['Loginmodel'].create(data)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
        return redirect('/')

    def login(self):
        data = {
        'email' : request.form['email'],
        'password': request.form['password']
        }
        status = self.models['Loginmodel'].check_login(data)
        if status:
            session['id'] = status['user']['id']
            session['name'] = status['user']['name']
        else:
            flash("Email or password does not exist")
        return redirect('/')

    def user_details(self, id):
        data = {
        'id': id
        }
        status = self.models['Loginmodel'].user_info(data)
        return self.load_view('userinfo.html', user=status['user_display'])

    def quotes(self):
        data = {
        'quote': request.form['quote'],
        'message': request.form['message'],
        'id': session['id']
        }
        quotes_information = self.models['Loginmodel'].quote(data)
        flash('Quote submitted')
        return redirect('/')

    def fav(self, quote_id):
        data = {
        'user_id' : session['id'], 
        'quote_id': quote_id
        }
        status = self.models['Loginmodel'].fav_info(data)
        return redirect('/')

    def delete(self, quote_id):
        data = {
        'user_id' : session['id'], 
        'quote_id': quote_id
        }
        status = self.models['Loginmodel'].remove(data)
        return redirect('/')



  


    






























       