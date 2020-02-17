import web
from web import form
from views.forms import get_task_form_elements, get_project_form_elements, get_user_form_elements, project_buttons
import models.project
import models.user
from views.utils import get_nav_bar, get_element_count

# Get html templates
render = web.template.render('templates/')

class New_project:

    def GET(self):
        """
        Get the project registration form
            
            :return: New project page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Retrive the required components to compose the form
        project_form_elements = get_project_form_elements()
        task_form_elements = get_task_form_elements()
        user_form_elements = get_user_form_elements()
        project_form = form.Form(*(project_form_elements + task_form_elements + user_form_elements))
        return render.new_project(nav, project_form, project_buttons,  "")

    def POST(self):
        """
        Create a new project

            :return: Redirect to main page
        """            
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Try the different URL input parameters to determine how to generate the form
        data = web.input(add_user=None, remove_user=None, 
            add_task=None, remove_task = None, create_project=None)

        # Add a set of task fields to the form
        if data.add_task:
            project_form = self.compose_form(data, "add_task")
            return render.new_project(nav, project_form, project_buttons,  "") 
        
        # Remove a set of task fields from the form
        if data.remove_task:
            project_form = self.compose_form(data, "remove_task")
            return render.new_project(nav, project_form, project_buttons,  "")     
        
        if data.add_user:
            project_form = self.compose_form(data, "add_user")
            return render.new_project(nav, project_form, project_buttons,  "")     
        
        if data.remove_user:
            project_form = self.compose_form(data, "remove_user")
            return render.new_project(nav, project_form, project_buttons,  "")    
            
        # Post the form data and save the project in the database
        if data.create_project:
                            
            project_form = self.compose_form(data, None)
            if not project_form.validates():
                return render.new_project(nav, project_form, project_buttons,  "")    

            task_count = get_element_count(data, "task_title_")
            user_count = get_element_count(data, "user_name_")

            # If there already are users assignet to the project the status will be set to in progress
            status = "open"
            if len(data.user_name_0):
                status = "in progress"

            # Validate the input user names
            for i in range(0, user_count):
                if len(data["user_name_"+str(i)]) and not models.user.get_user_id_by_name(data["user_name_"+str(i)]):    
                    return render.new_project(nav, project_form, project_buttons,  "Invalid user: " + data["user_name_"+str(i)])

            # Save the project to the database
            projectid = models.project.set_project(data.category_name, str(session.userid), 
            data.project_title, data.project_description, status)

            # Save the tasks in the database
            for i in range(0, task_count):
                models.project.set_task(str(projectid), (data["task_title_" + str(i)]), 
                (data["task_description_" + str(i)]), (data["budget_" + str(i)]))
                                
            # Save the users in the database given that the input field is not empty
            for i in range(0, user_count):
                    if len(data["user_name_"+str(i)]):
                        userid = models.user.get_user_id_by_name(data["user_name_"+str(i)])
                        read, write, modify = "FALSE", "FALSE", "FALSE"
                        try:
                            data["read_permission_"+str(i)]
                            read = "TRUE"
                        except Exception as e:
                            read = "FALSE"
                            pass
                        try:
                            data["write_permission_"+str(i)]
                            write = "TRUE"
                        except Exception as e:
                            write = "FALSE"
                            pass
                        try:
                            data["modify_permission_"+str(i)]
                            modify = "TRUE"
                        except Exception as e:
                            modify = "FALSE"
                            pass                        
                        models.project.set_projects_user(str(projectid), str(userid), read, write, modify)
            raise web.seeother('/?projects=my')
                        
    def compose_form(self, data, operation):
        """
        Compose a new project form by adding or removing a task

            :param data: The data object from web.input
            :param operation: Can be one of the four: add_task, add_user, remove_task, remove user
            :type operation: str
            :return: A project form object with all the required input fields
        """
        task_count = get_element_count(data, "task_title_")
        user_count = get_element_count(data, "user_name_")

        if operation == "remove_task" and task_count > 1:
            task_count -= 1
        if operation == "remove_user" and user_count >=1:
            user_count -= 1
        
        # Recreate project form fields
        project_form_elements = get_project_form_elements(data.project_title, data.project_description, data.category_name)

        # Recreate task form fields
        task_form_elements = ()
        for i in range(0, task_count):
            old_task_form_element = get_task_form_elements(i, data["task_title_"+str(i)], 
            data["task_description_"+str(i)], data["budget_"+str(i)])
            task_form_elements = (task_form_elements + old_task_form_element)

        # Recreate user form fields
        user_form_elements = ()
        for i in range(0, user_count):
            read, write, modify = False, False, False
            try:
                data["read_permission_"+str(i)]
                read = True
            except Exception as e:
                read = False
                pass
            try:
                data["write_permission_"+str(i)]
                write = True
            except Exception as e:
                write = False
                pass
            try:
                data["modify_permission_"+str(i)]
                modify = True
            except Exception as e:
                modify = False
                pass
            old_user_form_element = get_user_form_elements(i, data["user_name_"+str(i)], read, write, modify)
            user_form_elements = (user_form_elements + old_user_form_element)

        if operation == "add_task":
            new_task_form_elements = get_task_form_elements(task_count)    
            project_form = form.Form(*(project_form_elements + task_form_elements + new_task_form_elements + user_form_elements))
            return project_form

        if operation == "add_user":
            new_user_form_elements = get_user_form_elements(user_count)
            project_form = form.Form(*(project_form_elements + task_form_elements + user_form_elements + new_user_form_elements))
            return project_form

        project_form = form.Form(*(project_form_elements + task_form_elements + user_form_elements))
        return project_form
        