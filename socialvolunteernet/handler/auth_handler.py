import logging

from google.appengine.ext import webapp
import wsgiref.handlers
from socialvolunteernet.model.organization import Organization
from socialvolunteernet.model.volunteer import Volunteer

from google.appengine.ext.webapp import template

import time

class AuthenticationHandler(webapp.RequestHandler):

    def __init__(self, params):
        pass
    
    def post(self):
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        if action.lower() == 'new_organization':
            (success, params) = self.create_organization()
            if (success):
                params['type'] = 'organization'
                self.response.out.write(str(template.render("web/success.html", params)))
            else: 
                self.response.out.write(str(template.render("web/signup_organization.html", params)))
        elif action.lower() == 'new_volunteer':
            (success, params) = self.create_volunteer()
            if (success):
                params['type'] = 'volunteer'
                self.response.out.write(str(template.render("web/success.html", params)))
            else: 
                self.response.out.write(str(template.render("web/signup_volunteer.html", params)))
        else:
            self.response.out.write(str(template.render("web/login.html", {})))

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
        if not success:
            logging.error("Error adding new organization: %s" % repr(params))
        else:    
            logging.debug("Adding new organization: %s" % repr(params))

        return (success, params)
    
    def create_volunteer(self):
        params = {'error' : False,
                  'missing': [],
                  'id': str(int(time.time()))}
        self.parse_param('name', self.request.get('name'), params)
        self.parse_param('phone', self.request.get('phone'), params)
        self.parse_param('location', self.request.get('location'), params)
        self.parse_param('username', self.request.get('username'), params)
        
        ## This is junk
        #password = self.request.get('password1')
        
        if params['error']:
            logging.debug("Could not add new volunteer: the following fields were missing: "+repr(params['missing']))
            return (False, params)
        
        vol = Volunteer()
        success = vol.create_new(**params)
        if not success:
            logging.error("Error adding new volunteer: %s" % repr(params))
        else:    
            logging.debug("Adding new volunteer: %s" % repr(params))

        return (success, params)
    

    
    def parse_param(self, name, value, params):
        params[name] = value
        if not name:
            params['error'] = True
            params['missing'].append(name)                

        
def main():
    app = webapp.WSGIApplication([('login', AuthenticationHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()