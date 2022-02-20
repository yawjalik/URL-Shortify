# Methods for database interaction

import pymysql
from loguru import logger
import traceback
import os
from dotenv import load_dotenv

class Database:
    def __init__(self, host:str, username:str, password:str, database:str):
        try:
            self.db = pymysql.connect(host=host, user=username, password=password, database=database)
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
            logger.debug("Connected to DB")
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
            logger.debug("Closed DB connection")
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def retrieve(self, sql:str, args:list=[]):
        result = {}
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return result

    def execute(self, sql:str, args:list=[]):
        rows = 0
        try:
            rows = self.cursor.execute(sql, args)
            self.db.commit()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            self.db.rollback()
        finally:
            return rows

def main():
    load_dotenv()
    HOST=os.getenv("DB_HOST")
    USER=os.getenv("DB_USER")
    PASSWORD=os.getenv("DB_PASSWORD")
    DATABASE=os.getenv("DB_DATABASE")
    database = Database(HOST, USER, PASSWORD, DATABASE)
    row = database.retrieve("SHOW TABLES")
    logger.debug(row)
    

if __name__ == "__main__":
    main()