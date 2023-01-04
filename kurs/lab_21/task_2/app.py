from api import API
import json
from middleware import Middleware
from orm import Database

app = API()
db = Database()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)


@app.route("/posts?{data}")
def posts_params(request, response, data):
    method = request.method
    if method == "GET":
        response.text = found_posts_by_params(data)


@app.route("/posts/{data}")
def posts_work_by_id(request, response, data):
    method = request.method
    if method == "GET":
        response.text = get_post_by_id(data)
    elif method == "PUT":
        response.text = update_post_by_id(data, json.loads(request.body.decode("UTF-8")))
    elif method == "PATCH":
        response.text = patch_post_by_id(data, json.loads(request.body.decode("UTF-8")))
    elif method == "DELETE":
        response.text = delete_post_by_id(data)


@app.route("/posts/")
def posts(request, response):
    method = request.method
    if method == "GET":
        response.text = get_all_posts()
    elif method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        if type(data) is dict:
            response.text = insert_post(data)
        else:
            response.text = insert_many_posts(data)


def check_data(id_num=False, num_of_likes=False):
    if id_num is not False:
        if not str(id_num).isdigit():
            return 'No correct ID'
    if num_of_likes is not False:
        if not str(num_of_likes).isdigit():
            return 'No correct number of likes'


def get_post_by_id(id_num):
    check = check_data(id_num=id_num)
    if check:
        return check
    data = db.get_record_by_id(id_num)
    if data:
        return f"{json.dumps(data, indent = 5)}"
    return 'No data'


def update_post_by_id(id_num, body_data):
    check = check_data(id_num, num_of_likes=body_data['likes'])
    if check:
        return check
    data = db.update_record(id_num, body_data['title'], body_data['body'], body_data['likes'])
    if data:
        return f"{json.dumps(data, indent = 5)}"
    return 'Not found record to update'


def patch_post_by_id(id_num, body_data):
    title, body, likes = body_data.get('title', False), body_data.get('body', False), body_data.get('likes', False)
    if not any([title, body, likes]):
        return 'Not found column'
    check = check_data(id_num, num_of_likes=likes)
    if check:
        return check
    data = db.patch_update_record(id_num, title, body, likes)
    if data:
        return f"{json.dumps(data, indent = 5)}"
    return 'Not found record by id'


def found_posts_by_params(data):
    data = data.split("=")
    if len(data) != 2:
        return 'Not correct data'
    name_col, num_likes = data[0], data[1]
    check = check_data(num_of_likes=num_likes)
    if check:
        return check
    data = db.get_record_with_like(name_col, num_likes)
    if data:
        return f"{json.dumps(data, indent = 5)}"
    else:
        return 'No data'


def delete_post_by_id(id_num):
    check = check_data(id_num)
    if check:
        return check
    return db.delete_record(id_num)


def get_all_posts():
    data = db.get_all_records()
    if data:
        return f"{json.dumps(data, indent = 5)}"
    return 'No data'


def insert_post(body_data):
    title, body, likes = body_data.get('title', False), body_data.get('body', False), body_data.get('likes', False)
    if not any([title, body, likes]):
        return 'Not found data for all column'
    check = check_data(num_of_likes=likes)
    if check:
        return check
    data = db.add_new_record(title, body, likes)
    return f"{json.dumps(data, indent = 5)}"


def insert_many_posts(body_data):
    return db.add_many_new_record(body_data)
