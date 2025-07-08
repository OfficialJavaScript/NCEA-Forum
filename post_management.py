import json
from pathlib import Path

FORUM_FOLDER = Path("content/forum/")

def post_information(type, id):
    with open(f'content/{type}/{id}/post.json', 'r+') as post:
        post_data = json.load(post)
        if type != "forum":
            return post_data 
        post.close()
    with open(f'content/{type}/{id}/comments.json', 'r+') as comments:
        comments = json.load(comments)
        post.close()
    return ["forum", post_data, comments]

def write_post(post_information_var):
    for item in FORUM_FOLDER.iterdir():
        if item.is_dir():
            last_pid = int(str(item).replace('content\\forum\\', "")) 
    pid = last_pid + 1
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