from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 


class Job(object):

    def __init__(self, params):
        self.db = GoogleCloudSQLStore()
        
    # Creates a new job row in the database, corrected May 12 - www3
    CREATE_NEW = """
        INSERT INTO Job (organization_id, event_date, event_time, event_duration_minutes,
        score_value, description, title, category, status, location) VALUES
        (%(organization_id)s, %(date)s, %(time)s, %(duration)s, %(score)s, 
        %(description)s, %(title)s, %(category)s, 1, %(location)s)
    """
    INSERT_KEYWORD_CREATE = """
        INSERT INTO Keyword (keyword, reference_id) VALUES (%(keyword)s, LAST_INSERT_ID())        
    """
    def create_new(self, **kw):
        self.db.update(self.CREATE_NEW, kw)
        if kw['keywords']:
            for keyword in kw['keywords']:
                self.db.update(self.INSERT_KEYWORD, {'keyword': keyword})    
    
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
        DELETE FROM Keyword where keyword = %(keyword)s AND reference_id = %(job_id)s
    """
    INSERT_KEYWORD = """
        INSERT INTO Keyword (keyword, reference_id) VALUES (%(keyword)s, LAST_INSERT_ID())        
    """
    def edit_job(self, **kw):
        job_id = kw['job_id']
        self.db.update(self.EDIT_JOB, kw)
        keywords = set(kw['keywords'])
        word_list = self.db.select(self.GET_KEYWORDS, {'job_id': job_id})
        cur_keywords = set([k['keyword'] for k in word_list])
        new_kws = keywords - cur_keywords
        old_kws = cur_keywords - keywords
        if new_kws:
            logging.info("Adding keywords: "+repr(new_kws))
            for keyword in new_kws:
                self.db.update(self.INSERT_KEYWORD, {'keyword': keyword, 'job_id': job_id})
        if old_kws:
            logging.info("Removing keywords: "+repr(old_kws))
            for keyword in old_kws:
                self.db.update(self.DELETE_KEYWORD, {'keyword': keyword, 'job_id': job_id})                
                
    # Removes the job, or marks it inactive so that we can still return details about it
    DELETE_JOB = """
        UPDATE Job SET status=0 WHERE id=%(job_id)s
    """
    def delete_job(self, job_id):
        self.db.update(self.DELETE_JOB, {'job_id': job_id})
    
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
        logging.info("Job keywords "+repr([k['keyword'] for k in word_list]))
        info[0]['keywords'] = [k['keyword'] for k in word_list]
        return info
    
    # Add a volunteer to the committed volunteers, corrected May 12 - www3
    ADD_VOLUNTEER = """
        INSERT INTO Job_volunteer (job_id, volunteer_id, committed, completed, checkedin, checkedout, modified) 
        VALUES (%(job_id)s, %(volunteer_id)s, 1, 0, 0, 0, NOW())
    """
    def add_volunteer(self, volunteer_id, job_id):
        self.db.update(self.ADD_VOLUNTEER, {'job_id':job_id, 'volunteer_id':volunteer_id})
    
    # Move a volunteer status from committed to completed
    VOLUNTEER_COMPLETED = """
        UPDATE Job_volunteer SET completed=1, modified=NOW()  WHERE volunteer_id=%(volunteer_id)s
        AND job_id=%(job_id)s
    """
    # Corrected May 12 - www3
    UPDATE_SCORE = """
        INSERT INTO Score (id, job_id, score)
        VALUES (%(volunteer_id)s, %(job_id)s, %(score)s)
    """   
    def volunteer_completed(self, job_id, volunteer_id):
        self.db.update(self.VOLUNTEER_COMPLETED, {'job_id':job_id, 'volunteer_id':volunteer_id})
        logging.info('marked completed')
        job_info = self.get_info(job_id)
        logging.info('info: '+repr(job_info))
        self.db.update(self.UPDATE_SCORE, {'job_id':job_id, 'volunteer_id':volunteer_id, 'score':job_info[0]["score_value"]})

    # Move a volunteer status from committed to completed
    VOLUNTEER_CHECKIN = """
        UPDATE Job_volunteer SET checkedin=1, modified=NOW()  WHERE volunteer_id=%(volunteer_id)s
        AND job_id=%(job_id)s
    """  
    def volunteer_checkin(self, job_id, volunteer_id):
        self.db.update(self.VOLUNTEER_CHECKIN, {'job_id':job_id, 'volunteer_id':volunteer_id})

          
    # Remove the volunteer from the job
    DELETE_VOLUNTEER = """
        DELETE FROM Job_volunteer
        WHERE job_id=%(job_id)s AND volunteer_id=%(volunteer_id)s
    """
    def delete_volunteer(self, job_id, volunteer_id):
        self.db.update(self.DELETE_VOLUNTEER, {'job_id': job_id, 'volunteer_id':volunteer_id})
