import logging

from socialvolunteernet.model.organization import Organization
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import wsgiref.handlers
import time


class OrganizationHandler(webapp.RequestHandler):
        
    def post(self):
        
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        if not action:
            self.response.out.write(str(template.render("web/signup_organization.html", {})))
        if action.lower() == 'new_organization':
            (success, params) = self.create_organization()
            if (success):
                params['type'] = 'organization'
                self.response.out.write(str(template.render("web/success.html", params)))
            else: 
                self.response.out.write(str(template.render("web/signup_organization.html", params)))
                
    def get(self):
        logging.debug("Forwarding GET request to POST request")
        self.post()
            
    def create_organization(self):
        params = {'error' : False,
                  'missing': [],
                  'id': str(int(time.time()))}
        self.parse_param('name', self.request.get('name'), params)
        self.parse_param('phone', self.request.get('phone'), params)
        self.parse_param('location', self.request.get('location'), params)
        self.parse_param('description', self.request.get('description'), params)
        
        ## This is junk
        #password = self.request.get('password1')
        
        if params['error']:
            logging.debug("Could not add new organization: the following fields were missing: "+repr(params['missing']))
            return (False, params)
        
        org = Organization()
        success = org.create_new(**params)
        logging.debug("Adding new organization (success=%s) : %s" %(repr(success), repr(params)))

        return (success, params)
        
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