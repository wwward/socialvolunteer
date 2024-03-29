#!/usr/bin/env python

import wsgiref.handlers
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from socialvolunteernet.model.volunteer import Volunteer
from socialvolunteernet.model.job import Job

from google.appengine.api import users

class VolunteerHandler(webapp.RequestHandler):
        
    vol = Volunteer()  
    job = Job({})

    
    # Implemented by the parent class, but we don't want to support it....    
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
    
    def post(self):
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)
        logout = users.create_logout_url('/')
        
        if not action:
            self.response.out.write(str(template.render("web/signup_volunteer.html", {})))
            

        if not self.request.get('volunteer_id'):
            logging.error("Unknown volunteer_id! Cannot proceed!")
            raise Exception("Unknown volunteer_id")   
        
        volunteer_id = int(self.request.get('volunteer_id'))
        if action.lower() == 'delete_jobs':
            job_ids = self.request.get_all('cancel_job')
            self.cancel_jobs(volunteer_id, job_ids)
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'edit_jobs':
            data = self.get_job_display(volunteer_id)
            self.response.out.write(str(template.render("web/volunteer_jobs.html", data)))
        elif action.lower() == 'signup':
            job_id = self.request.get('job_id') 
            self.job.add_volunteer(volunteer_id, job_id)
            data = self.get_result_display(job_id, volunteer_id)
            data['kind'] = self.request.get('kind')
            data['keyword'] = self.request.get('keyword')
            data['category'] = self.request.get('category')
            data['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/jobs.html", data)))
        elif action.lower() == 'edit_friends':
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'delete_friends':
            friend_ids = [int(i) for i in self.request.get_all('friend_id')]
            self.delete_friends(volunteer_id, friend_ids)
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
        elif action.lower() == 'search_friends':
            query = self.request.get('search_friend')
            results = None
            if query:
                results = self.search_friends(volunteer_id, query)
            else:
                logging.info("No query term! Can't search!")
            data = self.get_friend_display(volunteer_id) 

            if query and not results:
                data["no_results"] = True
            else:
                data["search_results"] = results
            self.response.out.write(str(template.render("web/friends.html", data)))   
        elif action.lower() == 'add_friends':
            friend_ids = [int(i) for i in self.request.get_all('friend_id')]
            self.add_friends(volunteer_id, friend_ids)
            data = self.get_friend_display(volunteer_id)            
            self.response.out.write(str(template.render("web/friends.html", data)))
            
        elif action.lower() == 'edit_volunteer':
            data = self.get_volunteer_info(volunteer_id)
            data['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/edit_volunteer.html", data)))
        elif action.lower() == 'submit_edit_volunteer':
            #TODO: Verify the information
            name = self.request.get('name')
            phone = self.request.get('phone')
            location = self.request.get('location')
            email = self.request.get('email')

            missing = self.edit_volunteer(volunteer_id, name, phone, location, email)
            data = self.get_volunteer_info(volunteer_id)
            data['volunteer_id'] = volunteer_id
            if missing:
                data['missing'] = missing
            self.response.out.write(str(template.render("web/edit_volunteer.html", data)))
        elif action.lower() == 'portal':
            data = self.get_volunteer_portal(volunteer_id)
            data['volunteer_id'] = volunteer_id
            data['logout'] = logout
            self.response.out.write(str(template.render("web/volunteer.html", data)))
        
    def get_volunteer_portal(self, volunteer_id):    
        data = self.vol.get_info(volunteer_id)[0]
        data['friends'] =  self.vol.get_friends(volunteer_id)
        data['score'] = self.vol.get_score(volunteer_id)[0]['score']
        data['friend_scores'] = self.vol.get_friend_score(volunteer_id)
        data['global_scores'] = self.vol.get_global_scores()
        data['friend_activity'] = self.vol.get_friend_activity(volunteer_id)
        data['current_jobs'] = self.vol.get_current_jobs(volunteer_id)
        data['future_jobs'] = self.vol.get_future_jobs(volunteer_id)
        return data
    
    def get_volunteer_info(self, volunteer_id):
        return self.vol.get_info(volunteer_id)[0]
        
    def edit_volunteer(self, volunteer_id, name, phone, location, email):
        missing = []
        if not name:
            missing.append("name")
        if not phone:
            missing.append("phone")
        if not location:
            missing.append("location")
        if not email:
            missing.append("email")
        if not missing:
            self.vol.edit_volunteer_data(volunteer_id=volunteer_id, name=name, phone=phone, location=location, email=email)
        return missing 
        
    def cancel_jobs(self, volunteer_id, job_ids):
        for job_id in job_ids:
            if job_id: 
                self.vol.delete_job(volunteer_id, job_id)
                
    def add_friends(self, volunteer_id, friend_ids):
        friends = [i['id'] for i in self.get_friend_display(volunteer_id)['friends']]
        for friend_id in friend_ids:
            if friend_id and friend_id not in friends:
                self.vol.add_friend(volunteer_id, friend_id)

    def search_friends(self, volunteer_id, query):
        results =self.vol.get_volunteer_by_username(query, volunteer_id)
        return results
                 
    def delete_friends(self, volunteer_id, friend_ids):
        for friend_id in friend_ids:
            if friend_id:
                self.vol.remove_friend(volunteer_id, friend_id)

    def get_job_display(self, volunteer_id):
        data = {}
        data["volunteer_id"] = volunteer_id
        data["upcoming_jobs"] = self.vol.get_future_jobs(volunteer_id)
        data["current_jobs"] = self.vol.get_current_jobs(volunteer_id)
        data["past_jobs"] = self.vol.get_completed_jobs(volunteer_id)
        return data
    
    def get_result_display(self, job_id, volunteer_id):
        data = self.job.get_info(job_id)[0]
        status = self.vol.get_job_status(volunteer_id, job_id)
        if status:
            status = status[0]
        data['volunteer_status'] = status
        data['volunteer_id'] = volunteer_id
        logging.info(data)
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