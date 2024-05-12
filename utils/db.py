import json
import os
import random

#IF IT KEEPS CREAING NEW DB.JSON FILES, REMOVE "utils/" NEXT TO "db.json"

if os.path.exists("utils/db.json"):
    with open("utils/db.json", "r") as f:
        DB = json.load(f)
else:
    DB = {"admins": [], "message": "DEFAULT MESSAGE @OPENSOURCEFFA", "groups": [], "spam_time": 10, "phone_number": "", "voips": [], "voip_added": False}
    with open("db.json", "w+") as f:
        json.dump(DB, f)

def update():
    with open("utils/db.json", "w+") as f:
        json.dump(DB, f)

def get_random_proxy():
    with open("utils/proxies.txt", "r") as file:
        proxies = file.readlines()
    return random.choice(proxies).strip()

def get_session_string(phone_number):
    for voip in DB["voips"]:
        if voip.get("ph_num") == phone_number:
            return voip.get("session_string")
    return None

def groups_added():
    if not DB["groups"]:
        return False
    else:
        return True

def group_exist(id):
    if id in DB["groups"]:
        return True
    else: return False

def get_groups():
    return DB["groups"]

def get_phone_num():
    return DB["phone_number"]

def admin(id):
    if id in DB["admins"]:
        return False
    else:
        DB["admins"].append(id)
        update()
        return True
    
    
def unadmin(id):
    if id in DB["admins"]:
        DB["admins"].remove(id)
        update()
        return True
    else:
        return False

def set_message(message):
    try: 
        DB["message"] = message
        update()
        return True
    except Exception as e:
        return e

def get_message():
    return DB["message"]
    
def add_group(id):
    if id in DB["groups"]:
        return "Group already added"
    else:
        DB["groups"].append(id)
        update()
        return f"Group {id} added."

def remove_group(id):
    if id in DB["groups"]:
        DB["groups"].remove(id)
        update()
        return f"Group {id} removed."
    else:
        return "Group is not in the group list."

def set_time(time):
    try:
        DB["spam_time"] = int(time)
        update()
    except Exception as e:
        DB["spam_time"] = 10
        update()
        return f"An error has occured, the spam time has been reverted back to default settings.\nError: {e}"
    update()

def get_time():
    return DB["spam_time"]    

def add_voip(phone_number, session_string):
    new_entry = {"ph_num": phone_number, "session_string": session_string}

    for voip in DB["voips"]:
        if voip.get(phone_number) == phone_number:
            return f"VoIP {phone_number} already exists in the voips list."

    DB["voips"].append(new_entry)
    DB["voip_added"] = True
    DB["phone_number"] = phone_number
    update()
    return f"VoIP {phone_number} added to the voips list."

def remove_voip(phone_number):
    DB["phone_number"] = ""
    DB["voips"] = []
    DB["voip_added"] = False
    update()
    return f"Removed."

def is_voip_added():
    print(DB["voip_added"])
    return DB["voip_added"]

def is_admin(id):
    if id in DB["admins"]:
        return True
    else: 
        return False

def get_admins():
    return DB["admins"]
