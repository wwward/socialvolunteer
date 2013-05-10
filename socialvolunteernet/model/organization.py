from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 

class Organization(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
    
    CREATE_ORGANIZATION = """
        INSERT INTO Organization VALUES 
        (%(name)s, %(phone)s, %(email)s, %(location)s, 0, %(description)s )
    """
    def create_new(self, **kw):
        for key in ('id', 'name', 'phone', 'location', 'description'):
            if not key in kw:
                logging.error('Cannot create organization - missing field %s' % key)
                return False
        self.db.update(self.CREATE_ORGANIZATION, kw)
        return True;

    #Returns the total count of all jobs completed through the site for this organization
    # Status (0 = cancelled, 1 = incomplete, 2 = complete)
    GET_COMPLETED_JOB_COUNT = """
        select count(status) from groupwerk.Job 
        where organization_id = %(organization_id)s and status = 1
    """
    def get_completed_job_count(self, organization_id):
        return self.db.select(self.GET_COMPLETED_JOB_COUNT, 
                              {"organization_id": organization_id})
    
    #Returns all currently open job listings
    GET_CURRENT_JOBS = """
        select Job.*
        from Job
        WHERE Job.organization_id = %(organization_id)s
    """
    def get_current_jobs(self, organization_id):
        return self.db.select(self.GET_CURRENT_JOBS, 
                              {"organization_id": organization_id})
    
    # Returns all jobs that users have committed to, along with user_ids, maybe some user data
    GET_COMMITTED_JOBS = """
        select Job.title, Job.id, Job.event_date, Job.event_time, Job.location, Volunteer.name, Volunteer.username, Volunteer.id as volunteer_id
        from Job,Volunteer,Job_volunteer 
        WHERE Job.id = Job_volunteer.job_id 
        AND Job_volunteer.volunteer_id = Volunteer.id
        AND Job.organization_id = %(organization_id)s
        AND Job_volunteer.checkedin = 0
    """
    def get_committed_jobs(self, organization_id):
        return self.db.select(self.GET_COMMITTED_JOBS, 
                              {"organization_id": organization_id})
    
    # Returns all jobs that users have completed but have yet to be reviewed
    # Status 4 = reviewed
    GET_UNREVIEWED_JOBS = """
        select Job.title, Job.id, Job.event_date, Job.event_time, Job.location, Volunteer.name, Volunteer.username 
        from Job,Volunteer,Job_volunteer 
        WHERE Job.id = Job_volunteer.job_id 
        AND Job_volunteer.volunteer_id = Volunteer.id
        AND Job.organization_id = %(organization_id)s
        AND Job_volunteer.completed = 0
        AND Job_volunteer.checkedin = 1
    """
    def get_unreviewed_jobs(self, organization_id):
        return self.db.select(self.GET_UNREVIEWED_JOBS, 
                              {"organization_id": organization_id})
    
    # Returns all jobs that are completed and reviewed
    # Completed + Reviewed status = 5
    # Inactive status = 6
    GET_COMPLETED_JOBS = """
        select Job.title, Job.id, Job.event_date, Job.event_time, Job.location, Volunteer.name, Volunteer.username 
        from Job,Volunteer,Job_volunteer 
        WHERE Job.id = Job_volunteer.job_id 
        AND Job_volunteer.volunteer_id = Volunteer.id
        AND Job.organization_id = %(organization_id)s
        AND Job_volunteer.completed = 1
    """
    def get_completed_jobs(self, organization_id):
        return self.db.select(self.GET_COMPLETED_JOBS, 
                              {"organization_id": organization_id})
    
    # Get info about a given organization id
    GET_INFO = """
        select * from groupwerk.Organization 
        where id = %(organization_id)s
    """
    def get_info(self, organization_id):
        return self.db.select(self.GET_INFO,
                              {"organization_id": organization_id})
    
    # Delete a listed job
    DELETE_JOB = """
        delete from Job where organization_id = %(organization_id)s 
        AND job_id = %(job_id)s
    """
    def delete_job(self, organization_id, job_id):
        return self.db.select(self.DELETE_JOB,
                              {"organization_id": organization_id, "job_id": job_id})
    
    # Edit a listed job. Modified fields are in the kw dictionary
    EDIT_JOB = """
        UPDATE Job SET id=%(id)s, organization_id=%(organization_id)s, 
                       event_date=%(event_date)s, event_time=%(event_time)s,
                       event_duration_minutes=%(event_duration_minutes)s,
                       score_value=%(score_value)s, description=%(description)s,
                       category=%(category)s, status=%(status)s, title=%(title)s, 
                       location=%(location)s WHERE id=%(job_id)s AND organization_id=%(organization_id)s
    """
    def edit_job(self, organization_id, job_id, **kw):
        self.db.update(self.EDIT_JOB, kw)
    
    # Add a new job. The fields are in the kw dict
    ADD_JOB = """
       INSERT INTO Job VALUES (organization_id=%(organization_id)s, 
                       event_date=%(event_date)s, event_time=%(event_time)s,
                       event_duration_minutes=%(event_duration_minutes)s, title=%(title)s
                       score_value=%(score_value)s, description=%(description)s, location=%(location)s
                       category=%(category)s, status=%(status)s)
    """
    def add_job(self, **kw):
        self.db.update(self.ADD_JOB, kw)
        
    # Edit organization
    EDIT_ORGANIZATION = """
        UPDATE Organization SET name=%(name)s, email=%(email)s, phone=%(phone)s, location=%(location)s,
                                reputation=%(reputation)s, description=%(description)s
                                WHERE id=%(organization_id)s
    """
    def edit_organization_data(self, organization_id, **kw):
        self.db.update(self.EDIT_ORGANIZATION, kw)