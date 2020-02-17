import web
import models.project
from models.user import get_user_name_by_id
from views.utils import get_nav_bar, get_element_count
from views.forms import get_apply_form, get_apply_permissions_form

# Get html templates
render = web.template.render('templates/')

class Apply:

    def GET(self):
        """
        Get the apply view where users can sign up for a project
        """
        # Get session
        session = web.ctx.session
        # Get navbar
        nav = get_nav_bar(session)

        data = web.input(projectid=0)
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
        else:
            project = [[]]
            tasks = [[]]

        # Assemble form and set the user in context as an applicant with all permissions
        apply_form = get_apply_form()
        apply_permissions_form = get_apply_permissions_form()
        applicants = [[session.userid, session.username]]
        permissions = [["TRUE", "TRUE", "TRUE"]]
        render = web.template.render('templates/', globals={"get_apply_permissions_form":get_apply_permissions_form, 'session':session})

        return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants, permissions)

    def POST(self):
        """
        Post an application to the view, adding selected users to a project
        """
        data = web.input(projectid=0, add_user=None, remove_user=None, apply=None)
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Assemble form
        applicants = [session.username]
        apply_form = get_apply_form()
        apply_permission_form = get_apply_permissions_form()
        
        # Prepare globals
        render = web.template.render('templates/', globals={"get_apply_permissions_form":get_apply_permissions_form, 'session':session})
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)

            if data.add_user:
                applicants, permissions = self.get_applicants(data, "add_user")
                return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants,permissions)     

            elif data.remove_user:
                        applicants, permissions = self.get_applicants(data, "remove_user")
                        return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants, permissions)     
            
            # Set users as working on project and set project status in progress
            elif data.apply:
                applicants, permissions = self.get_applicants(data, "")
                for applicant, permission in zip(applicants, permissions):
                    models.project.set_projects_user(data.projectid, str(applicant[0]), permission[0], permission[1], permission[2])
                models.project.update_project_status(data.projectid, "in progress")
                raise web.seeother(('/project?projectid=' + str(data.projectid)))
                    
    def get_applicants(self, data, operation):
        """
        Get applicants and corresponding permissions from the input data with and operation
        :param data: Input data
        :param operation: Either empty, add_user or remove_user
        :type data: Storage
        :type operation: str
        """
        user_count = get_element_count(data, "user_")
        applicants = []
        permissions = []
        # Create the lists of current applying users and their permissions
        for i in range (0, user_count):
            applicant = data["user_"+str(i)][1:][:-1].split(",")
            applicants.append([ int(applicant[0]), applicant[1][2:][:-1] ])

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
            permissions.append([read, write, modify])

        if operation == "remove_user":
            user_to_remove = data.remove_user[1:][:-1].split(",")
            user_to_remove = [int(user_to_remove[0]), user_to_remove[1][2:][:-1]]
            for i in range (0, user_count):
                if user_to_remove == applicants[i]:
                    applicants.pop(i)
                    permissions.pop(i)
                    break

        elif operation == "add_user":
            user_id_to_add = data.user_to_add
            user_name_to_add = get_user_name_by_id(user_id_to_add)
            new_applicant = [ int(user_id_to_add), user_name_to_add ]
            if new_applicant not in applicants:
                applicants.append(new_applicant)
                permissions.append(["TRUE", "FALSE", "FALSE"])

        return applicants, permissions
            

