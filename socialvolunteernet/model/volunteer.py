
import logging

from socialvolunteernet.model.database import GoogleCloudSQLStore


class Volunteer(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
    
    CREATE_VOLUNTEER = """
        INSERT INTO Volunteer VALUES 
        (%(name)s, %(email)s, %(phone)s, %(location)s, '', 0, 0, %(username)s )
    """
    def create_new(self, **kw):
        for key in ('id', 'name', 'phone', 'location', 'username'):
            if not key in kw:
                logging.error('Cannot create volunteer - missing field %s' % key)
                return False
        self.db.update(self.CREATE_VOLUNTEER, kw)
        return True

    SELECT_BY_USERNAME = """
        SELECT * FROM Volunteer WHERE username = %(username)s and id <> %(id)s
    """
    def get_volunteer_by_username(self, username, volunteer_id):
        return self.db.select(self.SELECT_BY_USERNAME, {"username": username, "id": volunteer_id})
    
    # Adds a friend to the current volunteer
    ADD_FRIEND = """
        INSERT INTO Friends VALUES (%(volunteer_id)s, %(friend_volunteer_id)s)
    """
    def add_friend(self, volunteer_id, friend_volunteer_id):
        return self.db.update(self.ADD_FRIEND, {"volunteer_id": volunteer_id, "friend_volunteer_id": friend_volunteer_id})
    
    # Removes a friend from the current volunteer
    REMOVE_FRIEND = """ 
        DELETE FROM Friends WHERE id = %(volunteer_id)s AND friend_id = %(friend_volunteer_id)s
    """
    def remove_friend(self, volunteer_id, friend_volunteer_id):
        return self.db.update(self.REMOVE_FRIEND, {"volunteer_id": volunteer_id, "friend_volunteer_id": friend_volunteer_id})
    
    # Returns a list of friend data (all friend data, not just the id)
    GET_FRIENDS = """
        SELECT Volunteer.*  FROM Friends, Volunteer WHERE Friends.friend_id = Volunteer.id AND Friends.id = %(volunteer_id)s
    """
    def get_friends(self, volunteer_id):
        return self.db.select(self.GET_FRIENDS, {"volunteer_id": volunteer_id})
    
    # Returns my score
    GET_SCORE = """
        SELECT SUM(score) as score FROM Score WHERE id = %(volunteer_id)s
    """
    def get_score(self, volunteer_id):
        return self.db.select(self.GET_SCORE, {"volunteer_id": volunteer_id})
    
    # Returns a list of the scores of all of my friends
    GET_FRIEND_SCORE = """
        SELECT SUM(score) as score, Volunteer.* FROM Score, Volunteer WHERE Score.id IN (SELECT Friend_id FROM Friends WHERE Friends.id = %(volunteer_id)s) AND Score.id = Volunteer.id GROUP BY Score.id ORDER BY score DESC;
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
    GET_FRIEND_ACTIVITY = """
    SELECT Job_volunteer.*, Job.*, Volunteer.* FROM Job_volunteer, Job, Volunteer
    WHERE Job_Volunteer.volunteer_id IN (SELECT Friend_id FROM Friends WHERE Friends.id = %(volunteer_id)s)
    AND Job_Volunteer.volunteer_id = Volunteer.id
    AND Job_Volunteer.job_id = Job.id
    ORDER BY Job_Volunteer.modified DESC
    """
    def get_friend_activity(self, volunteer_id):
        return self.db.select(self.GET_FRIEND_ACTIVITY, {"volunteer_id": volunteer_id})

    
    # Returns a list of jobs that I have completed
    GET_COMPLETED_JOBS = """
        SELECT * FROM Job,Job_volunteer 
        WHERE Job.id = Job_volunteer.job_id
        AND Job_volunteer.volunteer_id = %(volunteer_id)s
        AND Job_volunteer.completed = 1
    """
    def get_completed_jobs(self, volunteer_id):
        return self.db.select(self.GET_COMPLETED_JOBS, {"volunteer_id": volunteer_id})
    
    # Returns a list of jobs that are in progress (e.g. I have been checked in but not checked out)
    GET_CURRENT_JOBS = """
        SELECT * FROM Job_volunteer, Job 
        WHERE Job_volunteer.job_id = Job.id AND Job_volunteer.checkedin = 1 
        AND Job_volunteer.checkedout != 1 AND Job_volunteer.volunteer_id = %(volunteer_id)s
    """
    def get_current_jobs(self, volunteer_id):
        return self.db.select(self.GET_CURRENT_JOBS, {"volunteer_id": volunteer_id})
    
    # Returns a list of the jobs that I have signed up for but not started
    GET_COMMITTED_JOBS = """
        SELECT * FROM Job,Job_volunteer 
        WHERE Job.id = Job_volunteer.job_id
        AND Job_volunteer.volunteer_id = %(volunteer_id)s
        AND Job_volunteer.committed = 1
        AND Job_volunteer.checkedin = 0
        AND Job_volunteer.completed = 0
        AND Job.status = 1
    """
    def get_future_jobs(self, volunteer_id):
        return self.db.select(self.GET_COMMITTED_JOBS, {"volunteer_id": volunteer_id})
    
    # Returns a job record, if it exists
    GET_JOB_STATUS = """
        SELECT job_id, committed, completed, checkedin FROM Job_volunteer 
        WHERE Job_volunteer.volunteer_id = %(volunteer_id)s
        AND Job_volunteer.job_id = %(job_id)s
    """
    def get_job_status(self, volunteer_id, job_id):
        return self.db.select(self.GET_JOB_STATUS, {"volunteer_id": volunteer_id, 'job_id': job_id})
    
    # Get volunteer information based on a volunteer_id
    GET_INFO = """
        SELECT * FROM Volunteer WHERE id = %(volunteer_id)s
    """
    def get_info(self, volunteer_id):
        return self.db.select(self.GET_INFO, {"volunteer_id": volunteer_id})
    
    # Edit user details, the modified fields are in the kw dictionary
    EDIT_VOLUNTEER_DATA = """
        UPDATE Volunteer
        SET name = %(name)s, phone = %(phone)s, location = %(location)s,
        email = %(email)s
        WHERE id = %(volunteer_id)s
    """
    def edit_volunteer_data(self, **kw):
        return self.db.update(self.EDIT_VOLUNTEER_DATA, kw)
    
    # Sign up for a new job
    ADD_JOB = """
        INSERT INTO Job_volunteer VALUES (%(job_id)s,%(volunteer_id)s,0,0, NOW());
    """
    def add_job(self, volunteer_id, job_id):
        return self.db.select(self.ADD_JOB, {"volunteer_id": volunteer_id, "job_id": job_id})
    
    # Delete a job. Note that you cannot delete things that you have been checked in or completed
    DELETE_JOB = """
        DELETE FROM Job_volunteer WHERE volunteer_id = %(volunteer_id)s
        AND completed = 0 AND checkedin = 0
    """
    def delete_job(self, volunteer_id, job_id):
        return self.db.update(self.DELETE_JOB, {"volunteer_id": volunteer_id, "job_id": job_id})
