import json

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