import logging 

class Organization(object):

    
    def create_new(self, **kw):
        logging.debug("Created %s " % repr(kw))
        return True;

    #Returns the total count of all jobs completed through the site for this organization
    def get_completed_job_count(self, organization_id):
        return 1234
    
    #Returns all currently open job listings
    def get_current_jobs(self, organization_id):
        return [{"job_id": "111", "name": "something"},
                {"job_id": "222", "name": "something else"}]
    
    # Returns all jobs that users have commited to, along with user_ids, maybe some user data
    def get_committed_volunteers(self, organization_id):
        return [{"volunteer_id": "1", "name": "BOB", "job_id": "123"},
               {"volunteer_id": "7", "name": "jim", "job_id": "456"} ]
    
    # Returns all jobs that users have completed but have yet to be reviewed
    def get_unreviewed_jobs(self, organization_id):
        return [{"job_id": "123", "volunteer_id": "7"},
                {"job_id": "456", "volunteer_id": "2"}]
    
    # Returns all jobs that are completed and reviewed
    def get_completed_jobs(self, organization_id):
        return [{"job_id": "444", "volunteer_id": "3"},
                {"job_id": "999", "volunteer_id": "5"}]
    
    # Get info about a given organization id
    def get_info(self, organization_id):
        return {"name": "my org", "description": "blah blah blah"}
    
    # Delete a listed job
    def delete_job(self, organization_id, job_id):
        logging.debug("Deleted job %s" % job_id)
        return True
    
    # Edit a listed job. Modified fields are in the kw dictionary
    def edit_job(self, organization_id, job_id, **kw):
        logging.debug("Edit job %s : %s" % (job_id, repr(kw)))
        return True
    
    # Add a new job. The fields are in the kw dict
    def add_job(self, **kw):
        logging.debug("Added job %s" % repr(kw))
        return True
    
    def edit_organization_data(self, organization_id, **kw):
        logging.debug("Added organization data %s : %s" %  (organization_id, repr(kw)))
        return True