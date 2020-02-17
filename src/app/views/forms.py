from web import form
from models.project import get_categories 
from models.user import get_users, get_user_id_by_name


# Regex for input validation
vemail = form.regexp(r".*@.*", "- Must be a valid email address")
vpass = form.regexp(r".{6,100}$", '- Must be atleast 6 characters long')
number = form.regexp(r"^[0-9]+$", "- Must be a number")
not_empty = form.regexp(r".+", "- This field is required")

# Define the login form 
login_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Checkbox("remember", description= "Remember me", checked=True, value=False),
    form.Button("Log In", type="submit", description="Login"),
)

# Define the register form 
register_form = form.Form(
    form.Textbox("username", not_empty, description="Username"),
    form.Textbox("full_name", not_empty, description="Full name"),
    form.Textbox("company", description="Company"),
    form.Textbox("email", vemail, description="Email Address"),
    form.Textbox("street_address", description="Street address"),
    form.Textbox("city", description="City"),
    form.Textbox("state", description="State"),
    form.Textbox("postal_code", number, description="Postal code"),
    form.Textbox("country", description="Country"),
    form.Password("password", vpass, description="Password"),
    form.Button("Register", type="submit", description="Register")
)

# Define the project view form
project_form = form.Form(
    form.Input("myfile", type="file"),
    form.Hidden("taskid"),
    form.Button("submit", type="submit", html="Upload"),
    form.Button("deliver", type="submit", value=True, html="Deliver"),
    form.Button("accepted", type="submit", value=True, html="Accept Delivery"),
    form.Button("declined", type="submit", value=True, html="Decline Delivery")
)

def get_task_form_elements(identifier=0, task_title="", task_description="", budget=""):
    """
    Generate a set of task form elements
        :param identifier: The id of the task
        :param task_title: Task title
        :param task_description: Task description 
        :param budget: Task budget
        :type identifier: int, str
        :type task_title: str
        :type task_description: str
        :type budget: int, str
        :return: A set of task form elements
    """
    task_form_elements = (
        form.Textbox("task_title_" + str(identifier), not_empty, description="Task title", value=task_title),
        form.Textarea("task_description_" + str(identifier), not_empty,description="Task description", value=task_description),
        form.Textbox("budget_" + str(identifier), number, description="Task budget", value=str(budget))
    )
    return task_form_elements

def get_project_form_elements(project_title="", project_description="", category_name=""):
    """
    Generate a set of project form elements
        :param project_title: Project title
        :param project_description: Project description 
        :param category_name: Name of the belonging category
        :type project_title: str
        :type project_description: str
        :type category_name: str
        :return: A set of project form elements    
    """
    categories = get_categories()
    project_form_elements = (
    form.Textbox("project_title", not_empty, description="Title", value=project_title),
    form.Textarea("project_description", not_empty, description="Description", value=project_description),
    form.Dropdown("category_name", description="Category", args=categories)
    )
    return project_form_elements

def get_user_form_elements(identifier=0, user_name="", read_permission=True, write_permission=False, modify_permission=False):
    """
    Get the user form elements used to set users in project upon creation
        :param identifier: The id of this element
        :param user_name: The current user
        :param read_permission: Permit user to read
        :param write_permission: Permit user to write
        :param modify_permission: Permit user to modify
        :type identifier: int
        :type user_name: str
        :type read_permission: bool
        :type write_permission: bool
        :type modify_permission: bool
        :return: The form elements to add users to a project
    """
    user_form_elements = (
        form.Textbox("user_name_" + str(identifier), description="User", value=user_name, placeholder="Leave blank for open project"),        
        form.Checkbox("read_permission_" + str(identifier), description="Read Permission", checked=read_permission, value=True),
        form.Checkbox("write_permission_" + str(identifier), description="Write Permission", checked=write_permission, value=True),
        form.Checkbox("modify_permission_" + str(identifier), description="Modify Permission", checked=modify_permission, value=True)
    )
    return user_form_elements

# Define buttons to modify the project form or create a project
project_buttons =  form.Form(
    form.Button("add_user", type="submit", description="Add User", value="add_user", html="Add User"),
    form.Button("remove_user", type="submit", description="Remove User", value="remove_user", html="Remove User"),
    form.Button("add_task", type="submit", description="Add Task", value="add_task", html="Add Task"),
    form.Button("remove_task", type="submit", description="Remove Task ", value="remove_task", html="Remove Task"),
    form.Button("create_project", type="submit", description="Create Project", value="create_project", html="Create Project")
)

def get_apply_form():
    """
    Get the form used to add users to an application and apply
        :return: A form object
    """
    users = get_users()
    apply_form = form.Form(
        form.Dropdown("user_to_add", description="User", args=users),
        form.Button("add_user", type="submit", description="Add User", value="add_user", html="Add User"),
        form.Button("apply", type="submit", description="Apply", value="apply", html="Apply")
    )
    return apply_form

def get_apply_permissions_form(identifier=0, read_permission="TRUE", write_permission="FALSE", modify_permission="FALSE", userid=None):
    """
    Get the form used to set permissions for each applicant
            :param identifier: The id of this element
            :param user_name: The current user
            :param read_permission: Permit user to read
            :param write_permission: Permit user to write
            :param modify_permission: Permit user to modify
            :type identifier: int
            :type user_name: str
            :type read_permission: bool
            :type write_permission: bool
            :type modify_permission: bool
            :return: A form object
    """
    user_permissions = form.Form(
        form.Button("remove_user", type="submit", description="User to remove", value=userid, html="X"),
        form.Hidden("user_"+str(identifier), description="User to apply for project", value=userid),
        form.Checkbox("read_permission_" + str(identifier), description="Read Permission", checked=(read_permission=="TRUE"), value=True),
        form.Checkbox("write_permission_" + str(identifier), description="Write Permission", checked=(write_permission=="TRUE"), value=True),
        form.Checkbox("modify_permission_" + str(identifier), description="Modify Permission", checked=(modify_permission=="TRUE"), value=True)
    )    
    return user_permissions
