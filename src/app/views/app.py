import os
import web
from views.utils import get_nav_bar
from views.login import Login
from views.logout import Logout
from views.register import Register
from views.new_project import New_project
from views.open_projects import Open_projects
from views.project import Project
from views.index import Index
from views.apply import Apply


# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/new_project', 'New_project',
    '/open_projects', 'Open_projects',
    '/project', 'Project',
    '/apply', 'Apply',
)
                              
# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

# Set session timeout
web.config.session_parameters['timeout'] = 15000000

# Workaround to use sessions with reloader (debugger) http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

# Add session to global variables
render._add_global(session, 'session')

# Make the session available cross modules through webctx
def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

app = app.wsgifunc()


