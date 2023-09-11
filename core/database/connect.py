from pymongo import MongoClient
import os, traceback, sys
sys.path.insert(0, "/backend/utils")
# from log import create_error_log

try:
    MONGODB_URL=os.getenv("MONGO_CONNECTION_STRING")
    client = MongoClient(MONGODB_URL)
    conn = client.get_database("checkinout")
except:
    print(traceback.format_exc())
    conn = None
    

if __name__ == "__main__":
    print(conn)