
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
    
    # Adds a friend to the current volunteer
    ADD_FRIEND = """
        INSERT INTO Friends VALUES (%(volunteer_id)s, %(friend_volunteer_id)s)
    """
    def add_friend(self, volunteer_id, friend_volunteer_id):
        return self.db.select(self.ADD_FRIEND, {"volunteer_id": volunteer_id, "friend_volunteer_id": friend_volunteer_id})
    
    # Removes a friend from the current volunteer
    REMOVE_FRIEND = """ 
        DELETE FROM Friends WHERE id = %(volunteer_id)s AND friend_id = %(friend_volunteer_id)s
    """
    def remove_friend(self, volunteer_id, friend_volunteer_id):
        return self.db.select(self.REMOVE_FRIEND, {"volunteer_id": volunteer_id, "friend_volunteer_id": friend_volunteer_id})
    
    # Returns a list of friend data (all friend data, not just the id)
    GET_FRIENDS = """
        SELECT * FROM Friends, Volunteer WHERE id = %(volunteer_id)s
    """
    def get_friends(self, volunteer_id):
        return self.db.select(self.GET_FRIENDS, {"volunteer_id": volunteer_id})
    
    # Returns my score
    GET_SCORE = """
        SELECT SUM(score) FROM Score WHERE id = %(volunteer_id)s
    """
    def get_score(self, volunteer_id):
        return self.db.select(self.GET_SCORE, {"volunteer_id": volunteer_id})
    
    # Returns a list of the scores of all of my friends
    GET_FRIEND_SCORE = """
        SELECT SUM(score) FROM Score WHERE id IN (SELECT Friend_id FROM Friends WHERE id = %(volunteer_id)s) GROUP BY id;
    """ 
    def get_friend_score(self, volunteer_id):
        return self.db.select(self.GET_FRIEND_SCORE, {"volunteer_id": volunteer_id})
    
    # Returns a list of scores of the top 10 users
    GET_GLOBAL_SCORES = """
        select Volunteer.username,SUM(Score.score) AS Total_Score from Volunteer,Score 
        WHERE Volunteer.id = Score.id 
        GROUP BY Volunteer.username 
        ORDER BY Total_Score DESC LIMIT 10
    """
    def get_global_scores(self):
        return self.db.select(self.GET_GLOBAL_SCORES)
    
    # Returns the top activity across the site
    # www3 - what constitutes activity?
    def get_friend_activity(self, volunteer_id):
        pass
    
    # Returns a list of jobs that I have completed
    def get_completed_jobs(self, volunteer_id):
        pass
    
    # Returns a list of jobs that are in progress (e.g. I have been checked in but not checked out)
    def get_current_jobs(self, volunteer_id):
        pass
    
    # Returns a list of the jobs that I have signed up for but not started
    def get_future_jobs(self, volunteer_id):
        pass
    
    # Get volunteer information based on a volunteer_id
    def get_info(self, volunteer_id):
        pass
    
    # Edit user details, the modified fields are in the kw dictionary
    def edit_volunteer_data(self, **kw):
        pass
    
    # Sign up for a new job
    def add_job(self, volunteer_id, job_id):
        pass
    
    # Delete a job. Note that you cannot delete things that you have been checked in or completed
    def delete_job(self, volunteer_id, job_id):
        pass
