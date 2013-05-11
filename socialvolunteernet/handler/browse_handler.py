from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import wsgiref.handlers

import logging

from socialvolunteernet.model.job import Job
from socialvolunteernet.model.browse import Browse
from socialvolunteernet.model.organization import Organization


class BrowseHandler(webapp.RequestHandler):
    '''
    Browse Handler
    '''
    
    brw = Browse()

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
    
    def search_by_keyword(self, keyword):
        missing = []
        if not keyword:
            missing.append("keyword")
        if not missing:
            self.brw.search_by_keyword(keyword)
        return missing
    
    def search_by_category(self, category):
        missing = []
        if not category:
            missing.append("category")
        if not missing:
            self.brw.search_by_category(category)
        return missing
    
    def parse_param(self, name, value, params):
        params[name] = value
        if not name:
            params['error'] = True
            params['missing'].append(name)
        
def main():
    app = webapp.WSGIApplication([('browse', BrowseHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()