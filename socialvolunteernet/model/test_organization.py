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
        return [{"job_id": "111", "name": "something", "description": "i dunno do something", "date": "05/13/2013"},
                {"job_id": "222", "name": "something else", "description": "KITTENS KITTENS KITTENS", "date": "05/26/2013"}]
    
    # Returns all jobs that users have commited to, along with user_ids, maybe some user data
    def get_committed_volunteers(self, organization_id):
        return [{"volunteer_id": "1", "volunteer_name": "BOB", "job_id": "123", "location": "spain", "date":"05/16/2013"},
               {"volunteer_id": "7", "volunteer_name": "jim", "job_id": "456", "location": "over there", "date": "05/19/2013"} ]
    
    # Returns all jobs that users have completed but have yet to be reviewed
    def get_unreviewed_jobs(self, organization_id):
        return [{"job_id": "123", "volunteer_id": "7", "volunteer_name": "Bob Smith", "job_name": "Feed ducks", "job_date": "05/12/2013"},
                {"job_id": "456", "volunteer_id": "2", "volunteer_name": "Jane Doe", "job_name": "Pet kittens", "job_date": "05/12/2013"}]
    
    # Returns all jobs that are completed and reviewed
    def get_completed_jobs(self, organization_id):
        return [{"job_id": "444", "volunteer_id": "3", "volunteer_name": "Jill", "date":"05/18/2013", "location":"madrid"},
                {"job_id": "999", "volunteer_id": "5", "volunteer_name": "Jack", "date": "05/23/2013", "location": "london"}]
    
    # Get info about a given organization id
    def get_info(self, organization_id):
        return {"name": "my org", "description": "blah blah blah", "organization_id": "1234", "location":"Texas", "phone": "12345"}
    
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