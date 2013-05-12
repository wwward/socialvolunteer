from socialvolunteernet.model.database import GoogleCloudSQLStore


class Browse(object):

    def __init__(self):
        self.db = GoogleCloudSQLStore()
        
    #search a job from database by selecting the keyword
    SEARCH_BY_KEYWORD = """
        SELECT Job.*
        FROM Job, Keyword
        WHERE Job.id = Keyword.reference_id AND Job.keyword = %(keyword)s
    """    
    def search_by_keyword(self, keyword):
        return self.db.select(self.SEARCH_BY_KEYWORD, keyword)
    
    #search a job from database by selecting the category
    SEARCH_BY_CATEGORY = """
        SELECT Job.*
        FROM Job
        WHERE Job.category = %(category)s
    """
    def search_by_category(self, category):
        return self.db.select(self.SEARCH_BY_CATEGORY, category)