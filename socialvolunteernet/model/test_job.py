import logging


class Job(object):

    def __init__(self, params):
        pass
        
    # Creates a new job row in the database
    def create_new(self, **kw):
        logging.debug("Created %s" % repr(kw))
        return True
    
    # Allows modification of information about the job
    def edit_job(self, job_id, **kw):
        logging.debug("Edited %s" % repr(kw))
        return True
    
    # Removes the job, or marks it inactive so that we can still return details about it
    def delete_job(self, job_id):
        logging.debug("Deleted %s" % job_id)
        return True
    
    # Returns a list of volunteers who have committed to the job, but not completed it
    def get_committed_volunteers(self, job_id):
        return [{"volunteer_id": "1", "name": "Bob", "location": "New York"}, 
                {"volunteer_id": "2", "name": "Kitteh", "location": "Joisey"}]
    
    # Returns a list of volunteers who have completed the job
    def get_completed_volunteers(self, job_id):
        return [{"volunteer_id": "1", "name": "Mr. Done", "location": "Doneville"}, 
                {"volunteer_id": "2", "name": "Donna", "location": "Done City"}]
    
    # Return info about a given job id
    def get_info(self, job_id):
        return {"name": "my organization", "description": "This is my description", "count": 1234,
                }
    
    # Add a volunteer to the committed volunteers
    def add_volunteer(self, job_id, volunteer_id):
        logging.debug("Added volunteer %s" % volunteer_id)
        return True
    
    # Move a volunteer status from committed to completed
    def volunteer_completed(self, job_id, volunteer_id):
        logging.debug("Marked %s as completed" % volunteer_id)
        return True
    
    # Remove the volunteer from the job
    def delete_volunteer(self, job_id, volunteer_id):
        logging.debug("Deleted volunteer %s" % volunteer_id)

        return True