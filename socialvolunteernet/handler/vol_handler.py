#!/usr/bin/env python

import wsgiref.handlers
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from socialvolunteernet.model.test_volunteer import Volunteer

class VolunteerHandler(webapp.RequestHandler):
        
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
    
    def post(self):
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        
        if not action:
            self.response.out.write(str(template.render("web/signup_volunteer.html", {})))
            
        volunteer_id = self.request.get('volunteer_id')
        if not volunteer_id:
            logging.error("Unknown volunteer_id! Cannot proceed!")
            raise Exception("Unknown volunteer_id")   
            
        if action.lower() == 'delete_jobs':
            # delete the job
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'edit_jobs':
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'edit_friends':
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'delete_friends':
            friend_id = self.request.get('friend_id')
            #self.delete_friend(volunteer_id, friend_id)
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'edit_volunteer':
            data = self.get_volunteer_info(volunteer_id)
            self.response.out.write(str(template.render("web/edit_volunteer.html", data)))
        elif action.lower() == 'portal':
            data = self.get_volunteer_portal(volunteer_id)
            data['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/volunteer.html", data)))
        
    def get_volunteer_portal(self, volunteer_id):
        vol = Volunteer()
        
        data = vol.get_info(volunteer_id)
        data['friends'] =  vol.get_friends(volunteer_id)
        data['score'] = vol.get_score(volunteer_id)
        data['friend_scores'] = vol.get_friend_score(volunteer_id)
        data['global_scores'] = vol.get_global_scores()
        data['friend_activity'] = vol.get_friend_activity(volunteer_id)
        data['current_jobs'] = vol.get_current_jobs(volunteer_id)
        data['future_jobs'] = vol.get_current_jobs(volunteer_id)
        
        return data
    
    def get_volunteer_info(self, volunteer_id):
        vol = Volunteer()
        return vol.get_info(volunteer_id)
    
    def get_job_display(self, volunteer_id):
        vol = Volunteer()
        data = {}
        data["volunteer_id"] = volunteer_id
        data["upcoming_jobs"] = vol.get_future_jobs(volunteer_id)
        data["current_jobs"] = vol.get_current_jobs(volunteer_id)
        data["past_jobs"] = vol.get_completed_jobs(volunteer_id)
        return data
    
    def get_friend_display(self,volunteer_id):
        vol = Volunteer()
        data = {}
        data["volunteer_id"] = volunteer_id
        data["friends"] = vol.get_friends(volunteer_id)
        return data
    
        
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