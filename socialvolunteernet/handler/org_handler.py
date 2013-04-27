import logging

from socialvolunteernet.model.test_organization import Organization
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import wsgiref.handlers


class OrganizationHandler(webapp.RequestHandler):
        
    def post(self):
        action = self.request.get('action')
        org_id = self.request.get('organization_id')
        logging.debug("Received POST request, action="+action)
        if not action:
            self.response.out.write(str(template.render("web/signup_organization.html", {})))
            
        if action.lower() == "complete_volunteers":
            #parse ids
            #self.volunteer_complete()
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "delete_job":
            #delete jobs
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "cancel_volunteer":
            #cancel volunteer
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "new_job":
            self.response.out.write(str(template.render("web/create_job.html", {"organization_id": org_id})))
        elif action.lower() == "submit_job":
            # DO NEW JOB WORK
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "edit_job":
            job_id = self.request.get('job_id')
            self.response.out.write(str(template.render("web/edit_job.html", {"organization_id" : org_id, 'job_id': job_id})))
        elif action.lower() == "edit_organization":
            self.response.out.write(str(template.render("web/edit_organization.html", {"organization_id" : org_id})))
        elif action.lower() == "portal":
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
                
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
            

    
    def get_organization_portal(self, organization_id):
        org = Organization()
        response = org.get_info(organization_id)
        response["current_commitments"] = org.get_unreviewed_jobs(organization_id)
        response["current_jobs"] = org.get_current_jobs(organization_id)
        response["upcoming_commitments"] = org.get_committed_volunteers(organization_id)
        response["completed_jobs"] = org.get_completed_jobs(organization_id)    
        return response
        
        
    def get_job_display(self):
        pass
    
    def volunteer_complete(self, volunteer_id):
        pass

    def add_job(self):
        pass
    
    
        
    def parse_param(self, name, value, params):
        params[name] = value
        if not name:
            params['error'] = True
            params['missing'].append(name)


def main():
    app = webapp.WSGIApplication([('/org', OrganizationHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()