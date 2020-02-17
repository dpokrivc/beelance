from models.database import db
import mysql.connector

def get_categories():
    """
    Get all categories

        :return: List of categories
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM project_category")
    try:
        cursor.execute(query)
        categories = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        categories = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return categories

def set_project(categoryid, userid, project_title, project_description, project_status):
    """
    Store a project in the database

        :param categoryid: The id of the corresponding category
        :param userid: The id of the project owner
        :param project_title: The title of the project
        :param project_description: The project description
        :param project_status: The status of the project
        :type categoryid: str
        :type userid: str
        :type project_title: str
        :type project_description: str 
        :type project_status: str
        :return: The id of the new project
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO projects VALUES (NULL, \"" + 
        categoryid + "\", \"" + userid + "\", \"" + project_title + "\", \"" + 
        project_description + "\", \"" + project_status + "\")")
    try:
        cursor.execute(query)
        db.commit()
        users_projects = get_projects_by_owner(userid) 
        projectid = users_projects[-1][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        projectid = None
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return projectid

def get_project_by_id(projectid):
    """
    Retrieve a project by its id

        :param projectid: The project id
        :type projectid: str
        :return: The selected project
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE projectid = \"" + projectid + "\"")
    try:
        cursor.execute(query)
        project = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        project = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return project[0]

def update_project_status(projectid, status):
    """
    Change the status of a selected project
        :param projectid: The project id
        :param status: The status to change to, should be either open, in progress or finished
        :type projectid: str
        :type status: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE projects SET project_status = \"" + status + 
        "\" WHERE projectid = \"" + projectid + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_user_permissions(userid, projectid):
    """
    Get permissions for a selected users in a specific project
        :param userid: The id of the user
        :param projectid: The id of the project
        :type userid: str
        :type projectid: str
        :return: Permissions as an array of numbers as boolean values
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT read_permission, write_permission, modify_permission \
        FROM projects_users WHERE projectid = \"" + projectid + 
        "\" AND userid = \"" + userid + "\"")
    try:
        cursor.execute(query)
        permissions = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    if len(permissions):
        return permissions[0]
    return [0,0,0]

def get_projects_by_status_and_category(categoryid, project_status):
    """
    Retrieve all projects from a category with a specific status

        :param catergoryid: The id of the category
        :param project_status: The status to filter on
        :type catergoryid: str
        :type project_status: str
        :return: A list of projects
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND categoryid = \"" + categoryid + "\"")
    try:
        cursor.execute(query)
        projects = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        projects = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return projects

def get_projects_by_owner(userid):
    """
    Retrieve all projects created by a specific user
        :param userid: The id of the user
        :type userid: str
        :return: An array of projects
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE userid = \"" + userid + "\"")
    try:
        cursor.execute(query)
        projects = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        projects = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return projects

def get_projects_by_status_and_owner(userid, project_status):
    """
    Retrieve all projects owned by a user with a specific status

        :param userid: The id of the owner
        :param project_status: The status to filter on
        :type userid: str
        :type project_status: str
        :return: A list of projects
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND userid = \"" + userid + "\"")
    try:
        cursor.execute(query)
        projects = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        projects = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return projects

def get_projects_by_participant_and_status(userid, project_status):
    """
    Retrieve all projects where the user is a participant with specific status

        :param userid: The id of the participant
        :param project_status: The status to filter on
        :type userid: str
        :type project_status: str
        :return: A list of projects
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM projects, projects_users WHERE projects.project_status = \"" + 
        project_status + "\" AND projects_users.userid = \"" + userid + 
        "\" AND projects_users.projectid = projects.projectid")
    db.connect()
    try:
        cursor.execute(query)
        projects = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        projects = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return projects

def set_task(projectid, task_title, task_description, budget):
    """
    Create a task

        :param projectid: The corresponding project id
        :param task_title: The title of the task
        :param task_description: The description of the task
        :param budget: The task budget
        :type projectid: str
        :type task_title: str
        :type task_description: str
        :type budget: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO tasks (projectid, title, task_description, budget, task_status) VALUES (\"" +
        projectid + "\", \"" + task_title + "\", \"" +
        task_description + "\", \"" + budget + "\", \"waiting for delivery\")")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
        
def update_task_status(taskid, status):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE tasks SET task_status = \"" + status + 
        "\" WHERE taskid = \"" + taskid + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_tasks_by_project_id(projectid):
    """
    Get all tasks belonging to a project

        :param project_id: The id of the project holding the tasks
        :type project_id: str
        :return: List of tasks
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT * FROM tasks WHERE projectid = \"" + projectid + "\"")
    try:
        cursor.execute(query)
        tasks = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        tasks = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return tasks

def set_task_file(taskid, filename):
    """
    Register a new task - file relationship

        :param taskid: The task id
        :param filename: The name of the file
        :type taskid: str
        :type filename: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO task_files (taskid, filename) VALUES (\"" + 
        taskid + "\", \"" + filename + "\")")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_task_files(taskid):
    """
        Retrieve all filenames registered in a task
        :param taskid: The task id
        :type taskid: str
        :return: An array of filenames
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT filename FROM task_files WHERE taskid = \"" + str(taskid) + "\"")
    try:
        cursor.execute(query)
        filenames = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        filenames = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return filenames

def set_projects_user(projectid, userid, read_permission="TRUE", 
        write_permission="NULL", modify_permission="NULL"):
    """
    Add a user to a project with specific permissions
        :param projectid: The project id
        :param userid: The user id
        :param read_permission: Describes whether a user can view information about a project
        :param write_permission: Describes whether a user can add files to tasks
        :param modify_permission: Describes wheter a user can deliver tasks
        :type projectid: str
        :type userid: str
        :type read_permission: str
        :type write_permission: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO projects_users VALUES (\"" + projectid + "\", \"" + 
        userid + "\", " + read_permission + ", " + 
        write_permission + ", " + modify_permission + ")")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
