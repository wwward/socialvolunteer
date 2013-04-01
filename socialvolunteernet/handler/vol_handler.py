#!/usr/bin/env python

import wsgiref.handlers
import logging
import time
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from socialvolunteernet.model.volunteer import Volunteer

class VolunteerHandler(webapp.RequestHandler):
        
    def get(self):
        logging.debug("Forwarding GET request to POST request")
        self.post()
    
    def post(self):
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        if not action:
            self.response.out.write(str(template.render("web/signup_volunteer.html", {})))
        if action.lower() == 'new_volunteer':
            (success, params) = self.create_volunteer()
            if (success):
                params['type'] = 'volunteer'
                self.response.out.write(str(template.render("web/success.html", params)))
            else: 
                self.response.out.write(str(template.render("web/signup_volunteer.html", params)))
                
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
    app = webapp.WSGIApplication([('/volunteer', VolunteerHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()