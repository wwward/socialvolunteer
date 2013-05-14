import logging

from google.appengine.ext import webapp
from socialvolunteernet.model.organization import Organization
from socialvolunteernet.model.volunteer import Volunteer
from google.appengine.ext.webapp import template
from google.appengine.api import users
import wsgiref.handlers
import time

class AuthenticationHandler(webapp.RequestHandler):
    
    # Google Authentication uses the GET method when passing a user.
    def get(self):
        user = users.get_current_user()
        if user:
            volunteer = Volunteer()
            org = Organization()
            if volunteer.get_info(user.user_id()):
                logging.info("FOUND VOLUNTEER")
                greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>) or \
                        <form action=\"volunteer\" method=\"post\">\
                        <input type=\"hidden\" name=\"action\" value=\"portal\" />\
                        <input type=\"hidden\" name=\"volunteer_id\" value=\"%s\" />\
                        <input type=\"Submit\" value=\"View volunteer portal\" class=\"button\" />\
                        </form>" % 
                        (user.nickname(), users.create_logout_url("/login"), user.user_id()))
            else:
                logging.info("DID NOT FIND VOLUNTEER")
                if org.get_info(user.user_id()):
                    logging.info("FOUND ORG")
                    greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)\
                            <form action=\"org\" method=\"post\">\
                            <input type=\"hidden\" name=\"action\" value=\"portal\"> \
                            <input type=\"hidden\" name=\"organization_id\" value=\"%s\" /> \
                            <input type=\"Submit\" value=\"View Organization portal\" class=\"button\" />\
                            </form>" % 
                            (user.nickname(), users.create_logout_url("/login"), user.user_id()))
                else:
                    logging.info("DID NOT FIND ORG")
                    greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>) Couldn't find you in the system!\
                                <form action=\"login\" method=\"post\">\
                                <input type=\"hidden\" name=\"action\" value=\"new_volunteer\" />\
                                <input type=\"hidden\" name=\"name\" value=\"%s\" />\
                                <input type=\"hidden\" name=\"location\" value=\"none\" />\
                                <input type=\"hidden\" name=\"phone\" value=\"none\" />\
                                <input type=\"hidden\" name=\"username\" value=\"%s\" />\
                                <input type=\"Submit\" value=\"Create New Volunteer\" class=\"button\" /> \
                                </form> or \
                                <form action=\"login\" method=\"post\">\
                                <input type=\"hidden\" name=\"action\" value=\"new_organization\" /> \
                                <input type=\"hidden\" name=\"name\" value=\"%s\" /> \
                                <input type=\"hidden\" name=\"location\" value=\"none\" /> \
                                <input type=\"hidden\" name=\"phone\" value=\"none\" /> \
                                <input type=\"hidden\" name=\"description\" value=\"%s\" /> \
                                <input type=\"Submit\" value=\"Create New Organization\" class=\"button\" /> \
                                </form>" % 
                            (user.nickname(), users.create_logout_url("/login"), user.nickname(), user.nickname(), user.nickname(),
                             user.nickname()))
            logging.info("Userid = " + user.user_id())
            
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/login"))

        self.response.out.write("<html><body>%s</body></html>" % greeting)
  
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
        user = users.get_current_user()
        params = {'error' : False,
                  'missing': [],
                  'id': user.user_id()}
        self.parse_param('name', user.nickname(), params)
        self.parse_param('phone', self.request.get('phone'), params)
        self.parse_param('location', self.request.get('location'), params)
        self.parse_param('description', user.nickname(), params)
        self.parse_param('email', user.email(), params)
        self.parse_param('reputation', 1, params)
        self.parse_param('id', user.user_id(), params)
        self.parse_param('organization_id', user.user_id(), params)
        
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
        user = users.get_current_user()
        params = {'error' : False,
                  'missing': [],
                  'id': user.user_id()}
        self.parse_param('name', user.nickname(), params)
        self.parse_param('phone', self.request.get('phone'), params)
        self.parse_param('location', self.request.get('location'), params)
        self.parse_param('username', user.nickname(), params)
        self.parse_param('email', user.email(), params)
        self.parse_param('reputation', 1, params)
        self.parse_param('id', user.user_id(), params)
        self.parse_param('volunteer_id', user.user_id(), params)
        
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
    app = webapp.WSGIApplication([('/login', AuthenticationHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()
