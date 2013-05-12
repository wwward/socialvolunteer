from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 


class Job(object):

    def __init__(self, params):
        self.db = GoogleCloudSQLStore()
        
    # Creates a new job row in the database
    CREATE_NEW = """
        INSERT INTO Job VALUES (organization_id=%(organization_id)s, 
                       event_date=%(date)s, event_time=%(time)s,
                       duration=%(duration)s,
                       score_value=%(scores, description=%(description)s,
                       title=%(title)s,category=%(category)s, status=%(status)s,
                       location=%(location)s)
    """
    INSERT_KEYWORD = """
        INSERT INTO Keyword VALUES (keyword=%(keyword)s, resource_id=%(resource_id)s)
    """
    def create_new(self, **kw):
        job_id = self.db.select(self.CREATE_NEW, kw)
        if kw['keywords']:
            for keyword in kw['keywords']:
                self.db.update(self.INSERT_KEYWORD, {'keyword': keyword, 'job_id': job_id})    
    
    # Allows modification of information about the job
    # Edit a listed job. Modified fields are in the kw dictionary
    EDIT_JOB = """
        UPDATE Job SET 
                       event_date=%(date)s, event_time=%(time)s,
                       event_duration_minutes=%(duration)s,
                       score_value=%(score)s, description=%(description)s,
                       category=%(category)s, status=%(status)s, title=%(title)s,
                       location=%(location)s, difficulty=%(difficulty)s
                       WHERE id=%(job_id)s AND organization_id=%(organization_id)s
    """
    DELETE_KEYWORD = """
        DELETE FROM Keyword where keyword = %(keyword)s AND job_id = %(job_id)s
    """
    def edit_job(self, **kw):
        job_id = kw['job_id']
        self.db.update(self.EDIT_JOB, kw)
        keywords = set(kw['keywords'])
        cur_keywords = set(self.GET_KEYWORDS({'job_id': job_id})[0]['keywords'])
        new_kws = keywords - cur_keywords
        old_kws = cur_keywords - keywords
        if new_kws:
            for keyword in new_kws:
                self.db.update(self.INSERT_KEYWORD, {'keyword': keyword, 'job_id': job_id})
        if old_kws:
            for keyword in old_kws:
                self.db.update(self.DELETE_KEYWORD, {'keyword': keyword, 'job_id': job_id})                
                
    # Removes the job, or marks it inactive so that we can still return details about it
    DELETE_JOB = """
        UPDATE Job SET status=6 WHERE job_id=%(job_id)s
    """
    def delete_job(self, job_id):
        self.db.update(self.DELETE_JOB, job_id)
    
    # Returns a list of volunteers who have committed to the job, but not completed it
    GET_COMMITTED_VOLUNTEERS = """
        SELECT volunteer_id FROM Job_volunteer WHERE committed=1 AND job_id=%(job_id)s
    """
    def get_committed_volunteers(self, job_id):
        return self.db.select(self.GET_COMMITTED_VOLUNTEERS, job_id)
    
    # Returns a list of volunteers who have completed the job
    GET_COMPLETED_VOLUNTEERS = """
        SELECT volunteer_id FROM Job_volunteer WHERE completed=1 AND job_id=%(job_id)s
    """
    def get_completed_volunteers(self, job_id):
        return self.db.select(self.GET_COMPLETED_VOLUNTEERS, job_id)
    
    # Return info about a given job id
    GET_INFO = """
       SELECT * FROM Job WHERE id=%(job_id)s
    """
    GET_KEYWORDS = """ 
       SELECT DISTINCT keyword FROM Keyword WHERE reference_id=%(job_id)s
    """
    def get_info(self, job_id):
        logging.info("Getting job info for "+repr(job_id))
        info = self.db.select(self.GET_INFO, {'job_id': job_id})
        word_list = self.db.select(self.GET_KEYWORDS, {'job_id': job_id})
        info[0]['keywords'] = [k['keyword'] for k in word_list]
        return info
    
    # Add a volunteer to the committed volunteers
    ADD_VOLUNTEER = """
        INSERT INTO Job_volunteer VALUES (volunteer_id=%(volunteer_id)s, modified=NOW())
        WHERE id=%(job_id)s
    """
    def add_volunteer(self, job_id, volunteer_id):
        self.db.update(self.ADD_VOLUNTEER, job_id, volunteer_id)
    
    # Move a volunteer status from committed to completed
    VOLUNTEER_COMPLETED = """
        UPDATE Job_volunteer SET completed=1, modified=NOW()  WHERE volunteer_id=%(volunteer_id)s
        AND job_id=%(job_id)s
    """
    UPDATE_SCORE = """
        INSERT INTO Score VALUES (id=%(volunteer_id)s, job_id=%(job_id)s, score=%(score)s)
    """
    def volunteer_completed(self, job_id, volunteer_id):
        self.db.update(self.VOLUNTEER_COMPLETED, {'job_id':job_id, 'volunteer_id':volunteer_id})
        logging.info('marked completed')
        job_info = self.get_info(job_id)
        logging.info('info: '+repr(job_info))
        self.db.update(self.UPDATE_SCORE, {'job_id':job_id, 'volunteer_id':volunteer_id, 'score':job_info[0]["score_value"]})
        
    
    # Remove the volunteer from the job
    DELETE_VOLUNTEER = """
        DELETE FROM Job_volunteer
        WHERE job_id=%(job_id)s AND volunteer_id=%(volunteer_id)s
    """
    def delete_volunteer(self, job_id, volunteer_id):
        self.db.update(self.DELETE_VOLUNTEER, job_id, volunteer_id)
