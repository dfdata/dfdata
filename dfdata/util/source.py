from dfdata.util import config

class Source:
    
    def __init__(self, kind):
        self.kind = kind
        self.name = self.kind
        self.db_name = self._get_db_name()
        self.table_name = config.defalut_config['table_name']
        
    def _get_db_name(self):
        db_name = config.get_db_name(self.kind)
        return db_name
    


    