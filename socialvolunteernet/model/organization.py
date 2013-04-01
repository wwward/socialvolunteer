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


        