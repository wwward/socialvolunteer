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
    
    #Returns all currently open job listings
    GET_CURRENT_JOBS = """
        select Job.*
        from Job
        WHERE Job.organization_id = %(organization_id)s
        AND Job.status = 1
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
        AND Job.status = 1
    """
    def get_committed_jobs(self, organization_id):
        return self.db.select(self.GET_COMMITTED_JOBS, 
                              {"organization_id": organization_id})
    
    # Returns all jobs that users have completed but have yet to be reviewed
    GET_UNREVIEWED_JOBS = """
        select Job.title, Job.id, Job.event_date, Job.event_time, Job.location, Volunteer.name, Volunteer.username, 
        Volunteer.id as volunteer_id
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
        
    # Edit organization
    EDIT_ORGANIZATION = """
        UPDATE Organization SET name=%(name)s, email=%(email)s, phone=%(phone)s, location=%(location)s,
                                 description=%(description)s
                                WHERE id=%(organization_id)s
    """
    def edit_organization_data(self, **kw):
        self.db.update(self.EDIT_ORGANIZATION, kw)