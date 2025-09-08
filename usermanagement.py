import json, random, base64

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_']

def exists(username):
    with open("database.json", 'r') as database:
        data = json.load(database)
        for user in data["USERS"]:
            if user["USERNAME"].lower() == username.lower():
                return user["ID"]
        return None
    
def exists_email(email):
    with open("database.json", 'r') as database:
        data = json.load(database)
        for user in data["USERS"]:
            if user["EMAIL"].lower() == email.lower():
                return user["ID"]

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
            if account["ID"] == uid:
                return account["PASSWORD"]
        else:
            return None

def role(uid):
    with open('database.json', 'r') as database:
        data = json.load(database)
        for account in data["USERS"]:
            if account["ID"] == uid:
                return account["ROLE"]
        else:
            return None
        
def create_code():
    code = ""
    for _ in range(6):
        code = f"{code}{random.randint(0,9)}"
    return code

def read_user_data(uid):
    with open('database.json', 'r') as database:
        data = json.load(database)
        for account in data["USERS"]:
            if account["ID"] == uid:
                return account
            
def check_verification(uid):
    data = read_user_data(uid)
    if data["CONFIRM_STATUS"] == "Unconfirmed":
        return "Unconfirmed"
    else:
        return "Confirmed"

def compare_verification(uid, code):
    data = read_user_data(uid)
    if data["CONFIRM_CODE"] == code:
        return True
    else:
        return False
    
def update_verification(uid, confirm_type, code):
    with open('database.json', 'r+') as database:
        data = json.load(database)
        for account in data["USERS"]:
            if account["ID"] == uid:
                database_id = data["USERS"].index(account)
                data["USERS"][database_id]["CONFIRM_STATUS"] = confirm_type
                data["USERS"][database_id]["CONFIRM_CODE"] = code
                database.seek(0)
                json.dump(data, database, sort_keys=True, indent=4)
                database.truncate()
                database.close()
    
def encode_user(uid, code, email_type):
    string = base64.b64encode((f'["{uid}", "{code}", "{email_type}"]').encode('utf-8')).decode('utf-8')
    return string

def decode_user(encoded_string):
    list = json.loads(base64.b64decode(encoded_string).decode('utf-8'))
    return list

def check_vcount(uid):
    data = read_user_data(uid)
    if int(data["LOGIN_COUNT"]) > 8:
        return "Reconfirm"
    else:
        return "Confirmed"
    
def update_vcount(uid, type):
    with open('database.json', 'r+') as database:
        data = json.load(database)
        for account in data["USERS"]:
            if account["ID"] == uid:
                database_id = data["USERS"].index(account)
                if type != "add":
                    data["USERS"][database_id]["LOGIN_COUNT"] = 0
                else:
                    data["USERS"][database_id]["LOGIN_COUNT"] = int(data["USERS"][database_id]["LOGIN_COUNT"]) + 1
                database.seek(0)
                json.dump(data, database, sort_keys=True, indent=4)
                database.truncate()
                database.close()
                
def get_email(uid):
    data = read_user_data(uid)
    return data["EMAIL"]

def read_name(uid):
    data = read_user_data(uid)
    return data["USERNAME"]

def username_check(username):
    for character in username:
        if character not in characters:
            return True
    return False

def get_pfp(uid):
    return read_user_data(uid)["PROFILE"]
