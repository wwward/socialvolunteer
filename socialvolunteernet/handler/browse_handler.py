

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
        
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
    
    def post(self):
        action = self.request.get('action')
        logging.debug("Received POST request, action="+action)

        volunteer_id = int(self.request.get('volunteer_id'))
        if action.lower() == 'category':
            category = self.request.get('category')
            if not category:
                data = {'volunteer_id': volunteer_id}
                self.response.out.write(str(template.render("web/show_categories.html", data)))
            else:
                results = self.search_by_category(category)
                results['volunteer_id'] = volunteer_id
                self.response.out.write(str(template.render("web/browse.html", results)))
        elif action.lower() == 'keyword':
            keyword = self.request.get('keyword')
            results = self.search_by_keyword(keyword)
            results['volunteer_id'] = volunteer_id
            self.response.out.write(str(template.render("web/search.html", results)))

    def search_by_keyword(self, keyword):
        # TODO : Do something if there is no keyword... perhaps forward back to the volunteer handler?
        results = self.brw.search_by_keyword(keyword)
        return results
    
    def search_by_category(self, category):
        results = self.brw.get_info()[0]
        results["category"] = self.brw.search_by_category(category)
        return results
    
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