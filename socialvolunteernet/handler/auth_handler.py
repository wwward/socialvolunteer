from google.appengine.ext import webapp
import wsgiref.handlers

class AuthenticationHandler(webapp.RequestHandler):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
def main():
    app = webapp.WSGIApplication([('login', AuthenticationHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()