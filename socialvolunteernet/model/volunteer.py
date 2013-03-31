'''
Created on Mar 29, 2013

@author: miria
'''

from google.appengine.ext import db

class Volunteer(db.Model):
    '''
    classdocs
    '''
    message = db.StringProperty()

    def __init__(self, params):
        '''
        Constructor
        '''
        