from google.appengine.ext import webapp
import wsgiref.handlers

import logging

class BrowseHandler(webapp.RequestHandler):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
        
def main():
    app = webapp.WSGIApplication([('browse', BrowseHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()