from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 


class Browse(object):

    def __init__(self, params):
        self.db = GoogleCloudSQLStore()
        
    #search a job from database by selecting the keyword
    SEARCH_BY_KEYWORD = """
        SELECT job by key word
    """    
    def search_by_keyword(self, key_word):
        return self.db.select(self.SEARCH_BY_KEYWORD, key_word)
    
    #search a job from database by selecting the category
    SEARCH_BY_CATEGORY = """
        SELECT job by category
    """
    def search_by_category(self, category):
        return self.db.select(self.SEARCH_BY_CATEGORY, category)