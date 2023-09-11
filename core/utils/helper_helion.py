import os 
import requests
import psycopg2
import traceback
import psycopg2.extras
import sys
sys.path.append("/core/utils/")
from log import Logger

# Get environment variables
HOSTNAME = os.getenv("HOSTNAME")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWD = os.getenv("PASSWD")
PORT = os.getenv("PORT")
SHIFT_QUERY = os.getenv("SHIFT_QUERY")

class Helper():
    def __init__(self, logger: Logger):
        connect = psycopg2.connect(
                host=HOSTNAME,
                dbname=DATABASE,
                user=USER,
                password=PASSWD,
                port=PORT)
        
        self.cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.logger = logger
                
    def get_shift_tier1(self):
        try:
            response = requests.get(url = f'http://{HOSTNAME}:8000/api/v1/shift_details/owner_current_shift?tier=1', 
                                         headers = {'accept': 'application/json'})
            current_shift = response.json()["current_shift"]
            current_tier1 = ""
            for user in current_shift:
                if user != "FIS.SRV":
                    current_tier1 = user
            response = requests.get(url = f'http://{HOSTNAME}:8000/api/v1/users/username/{current_tier1}', 
                                         headers = {'accept': 'application/json'})
            return response.json()["telegram"]
        
        except Exception as error:
            self.logger.log_message(error, "error")
            traceback.print_exception()
            return "@erikhorus"
        
    def get_alert_no_log(self) -> list:
        alert_no_log = []
        try:
            query_sql = """
                SELECT "public"."alert"."alert_name" AS "alert_name"
                FROM "public"."alert"
                WHERE CAST("public"."alert"."create_time" AS date) = CAST((CAST(now() AS timestamp) + (INTERVAL '-1 day')) AS date)
                    AND "public"."alert"."tenant" = 'BGT' AND lower("public"."alert"."alert_name") like '%no log%'
                ORDER BY "public"."alert"."create_time" DESC
                LIMIT 1048576
            """
            self.cursor.execute(query_sql)
            # Use list comprehension to extract only the alert names
            alert_no_log = [record[0] for record in self.cursor.fetchall()]
        except Exception as error:
            self.logger.log_message(error, "error")
            traceback.print_exception()
        return alert_no_log

    
if __name__ == "__main__":
    helper = Helper(logger=Logger())
    print(helper.get_shift_tier1())
    