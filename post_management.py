import json, threading, usermanagement
from pathlib import Path
from mailer import post_update

FORUM_FOLDER = Path("content/forum/")
GUIDE_FOLDER = Path("content/guide/")

def post_information(type, id):
    with open(f'content/{type}/{id}/post.json', 'r') as post:
        post_data = json.load(post)
        post.close()
    with open(f'content/{type}/{id}/comments.json', 'r') as comments:
        comments = json.load(comments)
        post.close()
    return [type, post_data, comments]

def write_post(post_information_var):
    post_list = []
    for item in FORUM_FOLDER.iterdir():
        if item.is_dir():
            post_list.append(int(str(item).replace('content\\forum\\', ""))) 
    post_list.sort()
    pid = post_list[-1] + 1
    folder = Path(f"content/forum/{pid}")
    folder.mkdir()
    with open(f"content/forum/{pid}/post.json", 'w') as post:
        file_info = post_information_var
        file_info["id"] = pid
        post.seek(0)
        json.dump(file_info, post, sort_keys=True, indent=4)
        post.truncate()
    with open(f"content/forum/{pid}/comments.json", 'w') as comments:
        file_info = {"comments": []}
        comments.seek(0)
        json.dump(file_info, comments, sort_keys=True, indent=4)
        comments.truncate()
    with open(f"content/forum/topics.json", 'r+') as topics:
        topic_data = json.load(topics)
        topic_data[post_information_var["topic"][0]].append(pid)
        topics.seek(0)
        json.dump(topic_data, topics, sort_keys=True, indent=4)
        topics.truncate()
        
def load_post(pid):
    with open(f"content/forum/{pid}/post.json", 'r+') as post:
        file_info = json.load(post)
        return file_info
    
def load_guide(pid):
    with open(f"content/guide/{pid}/post.json", 'r+') as post:
        file_info = json.load(post)
        return file_info

def load_comments(pid):
    with open(f"content/forum/{pid}/comments.json", 'r') as comments:
        comment_total = json.load(comments)
        return comment_total
        
def load_topic_posts(topic):
    with open("content/forum/topics.json", 'r') as topic_content:
        topics = json.load(topic_content)
        posts = topics[topic]
    post_info = []
    for post in posts:
        post_data = load_post(post)
        comments = load_comments(post)
        post_data["comments"] = len(comments["comments"])
        post_info.append(post_data)
    return post_info

def topic_total_posts():
    with open("content/forum/topics.json", 'r') as topic_file:
        topics = json.load(topic_file)
        topic_file.close()
    for topic in topics:
        topics[topic] = len(topics[topic])
    return topics

def check_if_exists(pid, post_type):
    if Path(f"content/{post_type}/{pid}").is_dir():
        return True
    else:
        return False
    
def add_comment(pid, post_type, content):
    with open(f"content/{post_type}/{pid}/comments.json", 'r+') as comment_file:
        comments = json.load(comment_file)
        comments["comments"].append(content)
        comment_file.seek(0)
        json.dump(comments, comment_file, sort_keys=True, indent=4)
        comment_file.truncate()
        comment_file.close()
        
def email_post_follower(pid, username, post_type, domain):
    with open(f"content/{post_type}/{pid}/post.json", 'r') as post_file:
        post_info = json.load(post_file)
        users = post_info["followers"]
        post_file.close()
    for user in users:
        if user[0].lower() != username.lower():
            notify_user = threading.Thread(target=post_update, args=(user[1], user[0], domain, load_post(pid)["title"], pid, username))
            notify_user.start()
            
def add_post_follow(pid, username, email):
    if [username, email] not in load_post(pid)["followers"]:
        with open(f"content/forum/{pid}/post.json", 'r+') as post_file:
            post_info = json.load(post_file)
            post_info["followers"].append([username, email])
            post_file.seek(0)
            json.dump(post_info, post_file, sort_keys=True, indent=4)
            post_file.truncate()
            post_file.close()
            
def remove_post_follow(pid, username, email):
    if [username, email] in load_post(pid)["followers"]:
        with open(f"content/forum/{pid}/post.json", 'r+') as post_file:
            post_info = json.load(post_file)
            post_info["followers"].remove([username, email])
            post_file.seek(0)
            json.dump(post_info, post_file, sort_keys=True, indent=4)
            post_file.truncate()
            post_file.close()
            
def retrieve_database_list():
    forum_post_list = []
    for item in FORUM_FOLDER.iterdir():
        if item.is_dir():
            forum_post_list.append(int(str(item).replace('content\\forum\\', ""))) 
    guide_post_list = []
    for item in GUIDE_FOLDER.iterdir():
        if item.is_dir():
            guide_post_list.append(int(str(item).replace('content\\guide\\', ""))) 
    forum_post_list.sort()
    guide_post_list.sort()
    return {
        "forum_post_list": forum_post_list,
        "guide_post_list": guide_post_list
    }

def compile_database(database_list):
    data = {
        "forum_post_data": [],
        "guide_post_data": []
    }
    for post in database_list["forum_post_list"]:
        info = load_post(post)
        data["forum_post_data"].append(info)
    for post in database_list["guide_post_list"]:
        info = post_information("guide", post)
        data["guide_post_data"].append([info[1], info[2]])
    return data

def search(query):
    database = compile_database(retrieve_database_list())
    posts = {
        "forum_posts": [],
        "guide_posts": []
    }
    for data in database["forum_post_data"]:
        if query.lower() in data["comment"].lower() or query.lower() in data["title"].lower():
            posts["forum_posts"].append(data["id"])
    for data in database["guide_post_data"]:
        if query.lower() in data[0]["comment"].lower() or query.lower() in data[0]["title"].lower() or query.lower() in data[1]["comments"][0]["content"].lower():
            posts["guide_posts"].append(data[0]["id"])
    return posts


def search_content_creator(search_results):
    posts = []
    for post in search_results["guide_posts"]:
        post_data = load_guide(post)
        post_data["type"] = "guide_post"
        posts.append(post_data)
        
    for post in search_results["forum_posts"]:
        post_data = load_post(post)
        post_data["comments"] = len(load_comments(post_data["id"])["comments"])
        post_data["type"] = "forum_post"
        posts.append(post_data)   
    return posts
