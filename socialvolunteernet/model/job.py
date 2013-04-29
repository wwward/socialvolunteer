

class Job(object):

    def __init__(self, params):
        pass
        
    # Creates a new job row in the database
    def create_new(self, **kw):
        pass
    
    # Allows modification of information about the job
    def edit_job(self, job_id, **kw):
        pass
    
    # Removes the job, or marks it inactive so that we can still return details about it
    def delete_job(self, job_id):
        pass
    
    # Returns a list of volunteers who have committed to the job, but not completed it
    def get_committed_volunteers(self, job_id):
        pass
    
    # Returns a list of volunteers who have completed the job
    def get_completed_volunteers(self, job_id):
        pass
    
    # Return info about a given job id
    def get_info(self, job_id):
        pass
    
    # Add a volunteer to the committed volunteers
    def add_volunteer(self, job_id, volunteer_id):
        pass
    
    # Move a volunteer status from committed to completed
    def volunteer_completed(self, job_id, volunteer_id):
        pass
    
    # Remove the volunteer from the job
    def delete_volunteer(self, job_id, volunteer_id):
        pass
