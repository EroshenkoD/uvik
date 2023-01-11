import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.Connection('crud.db')
        self.name_table = 'posts'

    def get_all_records(self):
        with self.connection as conn:
            res = []
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self.name_table} ;")
            data = cur.fetchall()
            if not data:
                return False
            for i in data:
                temp = {"id": i[0],
                        "title": i[1],
                        "body": i[2],
                        "likes": i[3]}
                res.append(temp)
            return res

    def create_database(self):
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.name_table}("
                        f"[id] INTEGER PRIMARY KEY NOT NULL,[title] TEXT NOT NULL,"
                        f"[body] TEXT NOT NULL, [likes] INTEGER NOT NULL);")
            conn.commit()

    def add_new_record(self, title, body, likes):
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO {self.name_table} VALUES (NULL, ?, ?, ?)", (title, body, likes))
            conn.commit()
            last_id = cur.lastrowid
            return self.get_record_by_id(last_id)

    def get_record_by_id(self, pk):
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self.name_table} WHERE id = ? ;", (pk,))
            data = cur.fetchall()
            if not data:
                return False
            data = data[0]
            res = {"id": data[0],
                   "title": data[1],
                   "body": data[2],
                   "likes": data[3]}
            return res

    def get_record_with_like(self, name_col, data_col):
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self.name_table} WHERE {name_col} = ? ;", (data_col,))
            data = cur.fetchall()
            if not data:
                return False
            res = []
            for i in data:
                temp = {"id": i[0],
                        "title": i[1],
                        "body": i[2],
                        "likes": i[3]}
                res.append(temp)
            return res

    def update_record(self, pk, title, body, likes):
        with self.connection as conn:
            check = self.get_record_by_id(pk)
            if not check:
                return False
            cur = conn.cursor()
            cur.execute(f"UPDATE {self.name_table} SET 'title' = ? , body = ?, likes = ? WHERE id = ?;",
                        (title, body, likes, pk))
            conn.commit()
            return self.get_record_by_id(pk)

    def patch_update_record(self, pk, title=False, body=False, likes=False):
        temp = self.get_record_by_id(pk)
        if not temp:
            return False
        title = temp['title'] if not title else title
        body = temp['body'] if not body else body
        likes = temp['likes'] if not likes else likes
        return self.update_record(pk, title, body, likes)

    def delete_record(self, pk):
        check = self.get_record_by_id(pk)
        if not check:
            return 'Not found record by id', 204
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {self.name_table} WHERE id = ?;", (pk,))
            conn.commit()
            return 'Record was deleted', 200

    def add_many_new_record(self, data):
        with self.connection as conn:
            try:
                cur = conn.cursor()
                for record in data:
                    title, body, likes = record['title'], record['body'], record['likes']
                    cur.execute(f"INSERT INTO {self.name_table} VALUES (NULL, ?, ?, ?);", (title, body, likes))
            except sqlite3.Error as e:
                conn.rollback()
                return str(e)
            except KeyError as e:
                conn.rollback()
                return f'Not found  key {e}', 204
            conn.commit()
            return 'Successfully', 201


if __name__ == "__main__":
    db = Database()
    db.create_database()
