#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import wsgiref.handlers

import logging

from socialvolunteernet.handler.vol_handler import VolunteerHandler
from socialvolunteernet.model.job import Job
from socialvolunteernet.model.browse import Browse
from socialvolunteernet.model.volunteer import Volunteer

class BrowseHandler(webapp.RequestHandler):
    '''
    Browse Handler
    '''
    
    brw = Browse()
    job = Job({})
    volunteer = Volunteer()
        
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
    
    def post(self):
        action = self.request.get('action').lower()
        kind = self.request.get('kind').lower()
        logging.info("Received POST request, action="+action+" kind="+kind)

        volunteer_id = int(self.request.get('volunteer_id'))
        if action == 'search' and kind == 'category':
            category = self.request.get('cur_category').strip()
            if not category:
                data = {}
                data['categories'] = self.get_category_list()
                data['volunteer_id'] =volunteer_id
                self.response.out.write(str(template.render("web/categories.html", data)))
            else:
                results = {}
                results['results'] = self.search_by_category(category)
                results['category'] = category
                results['volunteer_id'] = volunteer_id
                self.response.out.write(str(template.render("web/browse.html", results)))
        elif action == 'search' and kind == 'keyword':
            keyword = self.request.get('keyword').strip()
            if not keyword:
                volHandler = VolunteerHandler()
                data = volHandler.get_volunteer_portal(volunteer_id)
                data['volunteer_id'] = volunteer_id
                self.response.out.write(str(template.render("web/volunteer.html", data)))
            else: 
                data = {}
                data['results'] = self.search_by_keyword(keyword)
                data['keyword'] = keyword
                data['volunteer_id'] = volunteer_id
                self.response.out.write(str(template.render("web/search.html", data)))
        elif action == 'display': 
  
            job_id = int(self.request.get('job_id'))
            data = self.get_job_display(job_id, volunteer_id)
            data['kind'] = kind
            data['keyword'] = self.request.get('keyword')
            #data['category'] = self.request.get('category')
            data['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/jobs.html", data)))

    def search_by_keyword(self, keyword):
        results = self.brw.search_by_keyword(keyword)
        return results
    
    def search_by_category(self, category):
        results= self.brw.search_by_category(category)
        return results
    
    def get_category_list(self):
        categories = self.brw.get_category_list()
        #results = {}
        #for c in categories:
        #    results[c['category']] = c['count']
        return categories

    def get_job_display(self, job_id, volunteer_id):
        data = self.job.get_info(job_id)[0]
        status = self.volunteer.get_job_status(volunteer_id, job_id)
        if status:
            status = status[0]
        data['volunteer_status'] = status
        data['volunteer_id'] = volunteer_id
        return data
    
    def parse_param(self, name, value, params):
        params[name] = value
        if not name:
            params['error'] = True
            params['missing'].append(name)
        
def main():
    app = webapp.WSGIApplication([('/browse', BrowseHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()