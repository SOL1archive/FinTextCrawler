import MySQLdb

class Table:
    def __init__(self, db_name, table_name, data_list):
        self.db_name = db_name
        self.table_name = table_name
        self.data_list = data_list
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = MySQLdb.connect(
            user="kiron",
            passwd="kiron",
            host="localhost",
            db=self.db_name
        )

        self.cursor = self.conn.cursor()
    
    def insert(self, with_index=True):
        #테이블에 입력
        #f"INSERT INTO article VALUES({i+1},{self.total_row()})"
        for i, table_name in enumerate(self.data_list):
            self.cursor.execute(
                f"INSERT INTO {self.table_name} VALUES(" \
                + (str(i + 1) + ',' if with_index else '') \
                + table_name.total_row() + ')'
                )

    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()

    def commit_close(self):
        self.commit()
        self.close()
