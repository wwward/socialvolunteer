import logging

from socialvolunteernet.model.organization import Organization
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import wsgiref.handlers


class OrganizationHandler(webapp.RequestHandler):
        
    def post(self):
        
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        if not action:
            self.response.out.write(str(template.render("web/signup_organization.html", {})))
        if action.lower() == "complete_volunteers":
            pass
        elif action.lower() == "delete_jobs":
            pass
        elif action.lower() == "cancel_volunteer":
            pass
        elif action.lower() == "new_job":
            pass
        elif action.lower() == "edit_job":
            pass
                
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
            

    
    def get_organization_portal(self):
        data = []
        org = Organization()
        data["score"] = org.get_score()
        
        
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