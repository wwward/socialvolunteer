from google.appengine.api import rdbms

class GoogleCloudSQLStore(object):

    def __init__(self):
        INSTANCE_NAME="groupwerk:volunteerdb"
        DATABASE="volunteerdb"
        self._conn = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
        
    def select(self, sql, params=None):
        cursor = self._conn.cursor()
        cursor.execute(sql, params)

        # Convert from a list of lists to a list of maps where the key is the column name       
        rows = []
        column_names = self.get_columns(cursor)
        for row in cursor.fetchall():
            result = {}
            for i in range(0, len(row)):
                result[column_names[i]] = row[i]
            rows.append(result)
        cursor.close()
        return rows

    # Extract the column names from the cursor    
    def get_columns(self, cursor):
        names = []
        for (name, _,_,_,_,_,_) in cursor.description:
            names.append(name)
        return names
    
    def update(self, sql, params=None):
        cursor = self._conn.cursor()
        cursor.execute(sql,params)
        self._conn.commit()
        cursor.close()

    
