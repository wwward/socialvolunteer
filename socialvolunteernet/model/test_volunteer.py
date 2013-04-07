
import logging



class Volunteer(object):


    def create_new(self, **kw):
        logging.debug("Created new volunteer %s" % repr(kw))
        return True


    def get_volunteer_by_username(self, username):
        return {"name": "Dirk", "volunteer_id": "987", "username": username}
    
    # Adds a friend to the current volunteer
    def add_friend(self, volunteer_id, friend_volunteer_id):
        logging.debug("Added friends %s and %s" % (volunteer_id, friend_volunteer_id))
        return True
        

    def remove_friend(self, volunteer_id, friend_volunteer_id):
        logging.debug("Deleted friends %s and %s" % (volunteer_id, friend_volunteer_id))
        return True
        
    # Returns a list of friend data (all friend data, not just the id)
    def get_friends(self, volunteer_id):
        return [{"name": "buddy 1", "volunteer_id": "345", "username": "adsfasd"},
                {"name": "buddy 2", "volunteer_id": "222", "username": "adsfasdf"}]
    

    def get_score(self, volunteer_id):
        return 666
    
    # Returns a list of the scores of all of my friends
    def get_friend_score(self, volunteer_id):
        return [{"username": "asdfasd", "score": 324, "name": "winner"},
                {"username": "asdas", "score": 224, "name": "loser"}]
    

    def get_global_scores(self):
        return [{"username": "sssss", "score": 324000, "name": "GOD"},
                {"username": "kkkk", "score": 224000, "name": "KITTEH"}]
    
    # Returns the top activity across the site
    # www3 - what constitutes activity?
    def get_friend_activity(self, volunteer_id):
        return [] # Not sure what this will look like ATM
    
    # Returns a list of jobs that I have completed
    def get_completed_jobs(self, volunteer_id):
        return [{"job_id": "2342", "description": "hell if i know"}, 
                {"job_id": "3", "decription": "dunno"}]
    
    # Returns a list of jobs that are in progress (e.g. I have been checked in but not checked out)
    def get_current_jobs(self, volunteer_id):
        return [{"job_id": "222", "description": "right now"}, 
                {"job_id": "333", "decription": "current"}]
    
    # Returns a list of the jobs that I have signed up for but not started
    def get_future_jobs(self, volunteer_id):
        return [{"job_id": "999", "description": "future time"}, 
                {"job_id": "777", "decription": "laters"}]
    
    # Get volunteer information based on a volunteer_id
    def get_info(self, volunteer_id):
        return {"name": "this guy", "volunteer_id": volunteer_id, "location": "valhalla"}
    
    # Edit user details, the modified fields are in the kw dictionary
    def edit_volunteer_data(self, **kw):
        logging.debug("Edited volunteer %s" % repr(kw))
        return True
    
    # Sign up for a new job
    def add_job(self, volunteer_id, job_id):
        logging.debug("Added job %s to %s" % (job_id, volunteer_id)  )
        return True
    
    # Delete a job. Note that you cannot delete things that you have been checked in or completed
    def delete_job(self, volunteer_id, job_id):
        logging.debug("Delted job %s to %s " % (job_id, volunteer_id))
        return True
