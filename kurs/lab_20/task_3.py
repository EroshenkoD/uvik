import cgi
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pymongo import MongoClient
from random import randint


HOST_NAME = "localhost"
PORT = 8000
NAME_DB = 'blog'
NAME_COLLECTION = 'messages'


def show_records() -> str:
    with MongoClient() as client:
        res = '<center><br>'
        data = client[NAME_DB][NAME_COLLECTION].find().sort([('id_post', 1), ('creation_datetime', -1)])
        if len(list(data.clone())):
            for i in data:
                res += f"<h4>ID posts: {i['id_post']}, date: {i['creation_datetime']}," \
                       f" author: {i['author']}</h4><h4>message: {i['body']}</h4><br>"
        else:
            res += "<br><h2>No records</h2>"
        res += '<h2><a href="http://localhost:8000/">Main page</a></h2></center>'
        return res


def get_data_for_init(is_after_insert=False) -> str:
    res = ''
    if is_after_insert:
        res += "<br><center><h2>New record added successfully</h2></center>"
    res += """
        <center>
        <br><br>
        <h2><a href="http://localhost:8000/show">Show all message</a></h2>
        <br><br>
        <h2><a href="http://localhost:8000/add">Add new message</a></h2>
        </center>
        """
    return res


def get_data_for_add() -> str:
    res = """
    <center>
    <br><br>
        <h1>Add new message</h1>
    <form method="post" enctype="multipart/form-data">
    <br><br>
        <input type="Content-type" name="name" placeholder="Name">
    <br><br>
        <textarea type="Content-type" name="mess" placeholder="Message" rows="5"></textarea>
    <br><br>
        <input type="submit" value="Send">
    </form>
    </center>
    """
    return res


def insert_record(name: str, mess: str) -> None:
    with MongoClient() as client:
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M:%S")
        id_post = randint(0, 10)
        temp = {
            "id_post": id_post,
            "body": mess,
            "author": name,
            "creation_datetime": now
        }
        client[NAME_DB][NAME_COLLECTION].insert_one(temp)


class PythonServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            html = get_data_for_init()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        if self.path == '/add':
            html = get_data_for_add()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        if self.path == '/show':
            html = show_records()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        if self.path == '/add':
            c_type, p_dict = cgi.parse_header(self.headers.get('Content-Type'))
            p_dict['boundary'] = bytes(p_dict['boundary'], 'utf-8')
            p_dict['CONTENT-LENGTH'] = int(self.headers['content-length'])
            fields = cgi.parse_multipart(self.rfile, p_dict)
            insert_record(fields.get("name")[0], fields.get("mess")[0])
            html = get_data_for_init(is_after_insert=True)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))


if __name__ == "__main__":
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


