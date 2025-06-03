import json

def exists(UID):
    with open("database.json", 'r') as database:
        data = json.load(database)
        for users in data["USERS"]:
            if users["USERNAME"].lower() == UID.lower():
                return users["ID"]
        return None

def create_user_id():
    with open("database.json", 'r') as database:
        data = json.load(database)
        if not data["USERS"]:
            return "0"
        return int(data["USERS"][-1]["ID"]) + 1

def add_to_database(user):
    with open("database.json", 'r+') as database:
        data = json.load(database)
        data["USERS"].append(user)
        database.seek(0)
        json.dump(data, database, sort_keys=True, indent=4)
        database.truncate()

def hash(uid):
    with open("database.json", 'r') as database:
        data = json.load(database)
        for account in data["USERS"]:
            print(account)
            if account["ID"] == uid:
                return account["PASSWORD"]
        else:
            return None