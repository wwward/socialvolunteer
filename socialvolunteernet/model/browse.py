from socialvolunteernet.model.database import GoogleCloudSQLStore
import logging 


class Browse(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
        
    # Get info about all the jobs
    GET_INFO = """
        SELECT *
        FROM groupwerk.Job 
    """
    def get_info(self):
        return self.db.select(self.GET_INFO)
        
    #search a job from database by selecting the keyword
    SEARCH_BY_KEYWORD = """
        SELECT DISTINCT Job.*
        FROM Job, Keyword
        WHERE Job.id = Keyword.reference_id AND Keyword.keyword = %(keyword)s
    """    
    def search_by_keyword(self, keyword):
        return self.db.select(self.SEARCH_BY_KEYWORD, {'keyword': keyword})
    
    #search a job from database by selecting the category
    SEARCH_BY_CATEGORY = """
        SELECT DISTINCT Job.*
        FROM Job 
        WHERE Job.category = %(category)s
    """
    def search_by_category(self, category):
        return self.db.select(self.SEARCH_BY_CATEGORY, {"category": category})
    
    GET_CATEGORIES = """
        SELECT category, count(*) as count FROM Job group by category order by category
    """
    def get_category_list(self):
        return self.db.select(self.GET_CATEGORIES)