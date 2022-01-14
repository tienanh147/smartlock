
from pymongo.database import Database

def get_user(db: Database, username: str=''):
    return db["users"].find_one(
        {
            "$or":[
                {"username": username},
                {"email": username},
            ]
        })