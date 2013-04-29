from socialvolunteernet.model.database import GoogleCloudSQLStore


class Job(object):

    def __init__(self, params):
        self.db = GoogleCloudSQLStore()
        
    # Creates a new job row in the database
    CREATE_NEW = """
        INSERT INTO Job VALUES (id=%(id)s, organization_id=%(organization_id)s, 
                       event_date=%(event_date)s, event_time=%(event_time)s,
                       event_duration_minutes=%(event_duration_minutes)s,
                       score_value=%(score_value)s, description=%(description)s,
                       category=%(category)s, status=%(status)s)
    """
    def create_new(self, **kw):
        self.db.update(self.CREATE_NEW, kw)
    
    # Allows modification of information about the job
    # Edit a listed job. Modified fields are in the kw dictionary
    EDIT_JOB = """
        UPDATE Job SET id=%(id)s, organization_id=%(organization_id)s, 
                       event_date=%(event_date)s, event_time=%(event_time)s,
                       event_duration_minutes=%(event_duration_minutes)s,
                       score_value=%(score_value)s, description=%(description)s,
                       category=%(category)s, status=%(status)s 
                       WHERE id=%(job_id)s AND organization_id=%(organization_id)s
    """
    def edit_job(self, organization_id, job_id, **kw):
        self.db.update(self.EDIT_JOB, kw)
    
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
        self.db.update(self.GET_COMMITTED_VOLUNTEERS, job_id)
    
    # Returns a list of volunteers who have completed the job
    GET_COMPLETED_VOLUNTEERS = """
        SELECT volunteer_id FROM Job_volunteer WHERE completed=1 AND job_id=%(job_id)s
    """
    def get_completed_volunteers(self, job_id):
        self.db.update(self.GET_COMPLETED_VOLUNTEERS, job_id)
    
    # Return info about a given job id
    GET_INFO = """
       SELECT * FROM Job WHERE id=%(job_id)s
    """
    def get_info(self, job_id):
        self.db.update(self.GET_INFO, job_id)
    
    # Add a volunteer to the committed volunteers
    ADD_VOLUNTEER = """
        INSERT INTO Job_volunteer VALUES (volunteer_id=%(volunteer_id)s)
        WHERE id=%(job_id)s
    """
    def add_volunteer(self, job_id, volunteer_id):
        pass
    
    # Move a volunteer status from committed to completed
    VOLUNTEER_COMPLETED = """
        UPDATE Job_volunteer SET completed=1 WHERE volunteer_id=%(volunteer_id)s
        AND job_id=%(job_id)s
    """
    def volunteer_completed(self, job_id, volunteer_id):
        self.db.update(self.VOLUNTEER_COMPLETED, job_id)
    
    # Remove the volunteer from the job
    DELETE_VOLUNTEER = """
        DELETE FROM Job_volunteer
        WHERE job_id=%(job_id)s AND volunteer_id=%(volunteer_id)s
    """
    def delete_volunteer(self, job_id, volunteer_id):
        pass
