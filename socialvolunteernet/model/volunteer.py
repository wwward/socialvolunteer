
import logging

from socialvolunteernet.model.database import GoogleCloudSQLStore


class Volunteer(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
    
    CREATE_VOLUNTEER = """
        INSERT INTO Volunteer VALUES 
        (%(id)s, %(name)s, %(phone)s, %(location)s, '', 0, 0, %(username)s )
    """
    def create_new(self, **kw):
        for key in ('id', 'name', 'phone', 'location', 'username'):
            if not key in kw:
                logging.error('Cannot create volunteer - missing field %s' % key)
                return False
        self.db.update(self.CREATE_VOLUNTEER, kw)
        return True

    SELECT_BY_USERNAME = """
        SELECT * FROM Volunteer WHERE username = %(username)s
    """
    def get_volunteer_by_username(self, username):
        return self.db.select(self.SELECT_BY_USERNAME, {"username": username})
    
    def add_friend(self, volunteer_id, friend_volunteer_id):
        pass
    
    def remove_friend(self, volunteer_id, friend_volunteer_id):
        pass
    
    def get_friends(self, volunteer_id):
        pass
    
    def get_score(self, volunteer_id):
        pass
    
    def get_friend_score(self, volunteer_id):
        pass
    
    def get_global_scores(self):
        pass
    
    def get_friend_activity(self, volunteer_id):
        pass
    
    def get_completed_jobs(self, volunteer_id):
        pass
    
    def get_current_jobs(self, volunteer_id):
        pass
    
    def get_future_jobs(self, volunteer_id):
        pass