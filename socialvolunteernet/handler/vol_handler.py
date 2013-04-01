#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class VolunteerHandler(webapp.RequestHandler):
        
    def get(self):
        params = {}
        self.response.out.write(template.render("volunteer.html", params))
    
    def post(self):
        self.request.get('param')
        pass
    
def main():
    app = webapp.WSGIApplication([('vol', VolunteerHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()