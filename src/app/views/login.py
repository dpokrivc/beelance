import web
from views.forms import login_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64, pickle
import hashlib

# Get html templates
render = web.template.render('templates/')


class Login():

    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        self.check_rememberme()

        return render.login(nav, login_form, "")

    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", password="", remember=False)

        # Validate login credential with database query
        password_hash = hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest()
        user = models.user.match_user(data.username, password_hash)
        
        # If there is a matching user/password in the database the user is logged in
        if user:
            self.login(user[1], user[0], data.remember)
            raise web.seeother("/")
        else:
            return render.login(nav, login_form, "- User authentication failed")

    def login(self, username, userid, remember):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = userid
        if remember:
            rememberme = self.rememberme()
            web.setcookie('remember', rememberme , 300000000)

    def check_rememberme(self):
        """
        Validate the rememberme cookie and log in
        """
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            # Fetch the remember cookie and convert from string to bytes
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            # Decode the hash
            decode = base64.b64decode(remember_hash)
            # Load the decoded hash to receive the host signature and the username
            username, sign = pickle.loads(decode)
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.user.get_user_id_by_name(username)
            self.login(username, userid, False)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        return base64.b64encode(pickle.dumps(creds))

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 