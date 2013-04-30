#!/usr/bin/env python

import wsgiref.handlers
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from socialvolunteernet.model.volunteer import Volunteer

class VolunteerHandler(webapp.RequestHandler):
        
    vol = Volunteer()    
    
    # Implemented by the parent class, but we don't want to support it....    
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
            job_ids = self.request.get_all('cancel_job')
            self.cancel_jobs(volunteer_id, job_ids)
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'edit_jobs':
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'edit_friends':
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'delete_friends':
            friend_ids = self.request.get_all('friend_id')
            self.delete_friends(volunteer_id, friend_ids)
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'search_friends':
            query = self.request.get('search_friend')
            results = None
            if query:
                results = self.search_friends(volunteer_id, query)
            data = self.get_friend_display(volunteer_id) 

            if query and not results:
                data["no_results"] = True
            else:
                data["search_results"] = results
            logging.info(repr(data))          
            self.response.out.write(str(template.render("web/friends.html", data)))   
        elif action.lower() == 'add_friends':
            friend_ids = self.request.get_all('friend_id')
            self.add_friends(volunteer_id, friend_ids)
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
            
        elif action.lower() == 'edit_volunteer':
            data = self.get_volunteer_info(volunteer_id)
            self.response.out.write(str(template.render("web/edit_volunteer.html", data)))
        elif action.lower() == 'submit_edit_volunteer':
            #TODO: Verify the information
            name = self.request.get('name')
            phone = self.request.get('phone')
            location = self.request.get('location')
            missing = self.edit_volunteer(volunteer_id, name, phone, location)
            data = self.get_volunteer_info(volunteer_id)
            if missing:
                data['missing'] = missing
            self.response.out.write(str(template.render("web/edit_volunteer.html", data)))
        elif action.lower() == 'portal':
            data = self.get_volunteer_portal(volunteer_id)
            data['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/volunteer.html", data)))
        
    def get_volunteer_portal(self, volunteer_id):    
        data = self.vol.get_info(volunteer_id)
        data['friends'] =  self.vol.get_friends(volunteer_id)
        data['score'] = self.vol.get_score(volunteer_id)
        data['friend_scores'] = self.vol.get_friend_score(volunteer_id)
        data['global_scores'] = self.vol.get_global_scores()
        data['friend_activity'] = self.vol.get_friend_activity(volunteer_id)
        data['current_jobs'] = self.vol.get_current_jobs(volunteer_id)
        data['future_jobs'] = self.vol.get_current_jobs(volunteer_id)
        return data
    
    def get_volunteer_info(self, volunteer_id):
        return self.vol.get_info(volunteer_id)
        
    def edit_volunteer(self, volunteer_id, name, phone, location):
        missing = []
        if not name:
            missing.append("name")
        if not phone:
            missing.append("phone")
        if not location:
            missing.append("location")
        if not missing:
            self.vol.edit_volunteer_data(volunteer_id=volunteer_id, name=name, phone=phone, location=location)
            logging.info("EDIT VOLUNTEER "+volunteer_id+" "+name+" "+phone+" "+location)
        return missing 
        
    def cancel_jobs(self, volunteer_id, job_ids):
        for job_id in job_ids:
            if job_id: 
                self.vol.delete_job(volunteer_id, job_id)
                logging.info("DELETED JOBS "+volunteer_id+" "+job_id)
                
    def add_friends(self, volunteer_id, friend_ids):
        for friend_id in friend_ids:
            if friend_id:
                self.vol.add_friend(volunteer_id, friend_id)
                logging.info("ADDED FRIEND "+volunteer_id+" "+friend_id)

    def search_friends(self, volunteer_id, query):
        results = []
        #TODO: we need a friend search
        #results =self.vol.find_friends(volunteer_id, query)
        logging.info("TODO: SEARCH FRIENDS "+volunteer_id+" "+query+" num results: "+str(len(results)))
        return results
                 
    def delete_friends(self, volunteer_id, friend_ids):
        for friend_id in friend_ids:
            if friend_id:
                self.vol.remove_friend(volunteer_id, friend_id)
                logging.info("DELETED FRIEND "+volunteer_id+" "+friend_id)

    def get_job_display(self, volunteer_id):
        data = {}
        data["volunteer_id"] = volunteer_id
        data["upcoming_jobs"] = self.vol.get_future_jobs(volunteer_id)
        data["current_jobs"] = self.vol.get_current_jobs(volunteer_id)
        data["past_jobs"] = self.vol.get_completed_jobs(volunteer_id)
        return data
    
    def get_friend_display(self,volunteer_id):
        data = {}
        data["volunteer_id"] = volunteer_id
        data["friends"] = self.vol.get_friends(volunteer_id)
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