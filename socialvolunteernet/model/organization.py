from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 

class Organization(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
    
    CREATE_ORGANIZATION = """
        INSERT INTO Organization VALUES 
        (%(id)s, %(name)s, %(phone)s, %(location)s, 0, %(description)s )
    """
    def create_new(self, **kw):
        for key in ('id', 'name', 'phone', 'location', 'description'):
            if not key in kw:
                logging.error('Cannot create organization - missing field %s' % key)
                return False
        self.db.update(self.CREATE_ORGANIZATION, kw)
        return True;

    #Returns the total count of all jobs completed through the site for this organization
    def get_completed_job_count(self, organization_id):
        pass
    
    #Returns all currently open job listings
    def get_current_jobs(self, organization_id):
        pass
    
    # Returns all jobs that users have commited to, along with user_ids, maybe some user data
    def get_committed_jobs(self, organization_id):
        pass
    
    # Returns all jobs that users have completed but have yet to be reviewed
    def get_unreviewed_jobs(self, organization_id):
        pass
    
    # Returns all jobs that are completed and reviewed
    def get_completed_jobs(self, organization_id):
        pass
    
    # Get info about a given organization id
    def get_info(self, organization_id):
        pass
    
    # Delete a listed job
    def delete_job(self, organization_id, job_id):
        pass
    
    # Edit a listed job. Modified fields are in the kw dictionary
    def edit_job(self, organization_id, job_id, **kw):
        pass
    
    # Add a new job. The fields are in the kw dict
    def add_job(self, **kw):
        pass
    
    def edit_organization_data(self, organization_id, **kw):
        pass