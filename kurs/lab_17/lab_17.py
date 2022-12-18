"""Blog
Create the scheme for the Personal Blog. Create the Database, tables, views(at least 1).

Add constraints, indexes. Add the field for saving photos/files for each blog's post.

Note: Use any RDBMS that you want. Use at least 4 tables.

Bonus task: fill the tables with the data from csv files
"""
import csv
import pandas as pd
import psycopg2
from datetime import timedelta
from mimesis import Generic
from random import randint
from kurs.lab_17.config import database, user, password, host, port


def write_file_csv(path_with_name: str, columns: tuple, data: list) -> None:
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path_with_name)


def create_all_table_in_data_base_from_file(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        curr.execute(open("schema.sql", "r").read())
        conn.commit()


def delete_all_data_from_data_base(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        curr.execute(f"DROP VIEW IF EXISTS main_information_by_users")
        conn.commit()
        curr.execute(f"DROP INDEX IF EXISTS index_post_category_with_creation_date")
        curr.execute(f"DROP EXTENSION IF EXISTS pgcrypto")
        list_name_bd = get_name_all_table(conn)
        for name_bd in list_name_bd:
            curr.execute(f"DROP TABLE {name_bd} CASCADE")
        conn.commit()


def get_name_all_table(conn: psycopg2) -> list:
    res = []
    with conn.cursor() as curr:
        curr.execute('''SELECT table_name FROM information_schema. tables 
        WHERE table_schema NOT IN ('information_schema','pg_catalog')''')
        for row in curr.fetchall():
            res.append(row[0])
        return res


def create_file_with_data_for_table_users(num_user: int) -> None:
    path_to_photo = './avatar/avatar.jpg'
    columns = ('first_name', 'last_name', 'phone', 'email', 'password_hash',
               'registration_date', 'last_login', 'path_to_photo')
    data = []
    for i in range(num_user):
        random_data = Generic('en')
        last_login = random_data.datetime.datetime() + timedelta(days=i)
        temp = [random_data.person.first_name(), random_data.person.last_name(), random_data.person.telephone(),
                random_data.person.email(), random_data.person.password(),
                random_data.datetime.datetime(), last_login, path_to_photo]
        data.append(temp)
        write_file_csv('./csv_files/users.csv', columns, data)


def insert_data_from_csv_file_to_table_users(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        with open('./csv_files/users.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                temp = (row['first_name'], row['last_name'], row['phone'], row['email'], row['password_hash'],
                        row['registration_date'], row['last_login'], row['path_to_photo'])
                curr.execute('''
                INSERT INTO users (
                first_name, last_name, phone, email, password_hash, registration_date, last_login, path_to_photo
                ) 
                VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s) RETURNING id_user''', temp)
                conn.commit()
                id_user = curr.fetchall()[0][0]
                insert_data_permission_for_user(id_user, conn)


def insert_data_permission_for_user(id_user: int, conn: psycopg2) -> None:
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM typePermission")
        all_permission = curr.fetchall()
        temp = (id_user, all_permission[randint(0, len(all_permission) - 1)][0])
        curr.execute("INSERT INTO userPermission (user_id, type_permission_id) VALUES (%s, %s)", temp)
        conn.commit()


def create_file_with_data_for_table_posts(num_posts: int, conn: psycopg2) -> None:
    columns = ('user_id', 'category_id', 'title', 'body', 'creation_date', 'validity_date')
    data = []
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM users")
        all_users = curr.fetchall()
        curr.execute("SELECT * FROM categories")
        all_categories = curr.fetchall()
        for i in range(num_posts):
            random_data = Generic('en')
            user_id = all_users[randint(0, len(all_users) - 1)][0]
            category_id = all_categories[randint(0, len(all_categories) - 1)][0]
            validity_date = random_data.datetime.datetime() + timedelta(days=i)
            temp = [user_id, category_id, random_data.text.title(), random_data.text.text(),
                    random_data.datetime.datetime(), validity_date]
            data.append(temp)
            write_file_csv('./csv_files/posts.csv', columns, data)


def insert_data_all_posts_and_add_photo(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        with open('./csv_files/posts.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                temp = (row['user_id'], row['category_id'], row['title'], row['body'],
                        row['creation_date'], row['validity_date'])
                curr.execute('''INSERT INTO posts (
                user_id, category_id, title, body, creation_date, validity_date
                ) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_post''', temp)
                conn.commit()
                post_id = curr.fetchall()[0][0]
                create_file_with_data_for_table_photos(randint(1, 5), post_id)
                insert_data_with_photos_for_posts(conn)


def create_file_with_data_for_table_photos(num_photos: int, post_id: int) -> None:
    columns = ('post_id', 'path_to_photo')
    path_to_photo = './post_photo/post_photo.jpg'
    data = []
    for i in range(num_photos):
        temp = [post_id, path_to_photo]
        data.append(temp)
    write_file_csv('./csv_files/photos.csv', columns, data)


def insert_data_with_photos_for_posts(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        with open('./csv_files/photos.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                temp = (row['post_id'], row['path_to_photo'])
                curr.execute("INSERT INTO photos (post_id, path_to_photo) VALUES (%s, %s)", temp)
        conn.commit()


def create_file_with_data_for_table_comments_user(num_comments: int, conn: psycopg2) -> None:
    columns = ('user_id', 'post_id', 'body', 'creation_date')
    data = []
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM users")
        all_users = curr.fetchall()
        curr.execute("SELECT * FROM posts")
        all_posts = curr.fetchall()
        for i in range(num_comments):
            random_data = Generic('en')
            user_id = all_users[randint(0, len(all_users) - 1)][0]
            post_id = all_posts[randint(0, len(all_posts) - 1)][0]
            temp = [user_id, post_id, random_data.text.title(), random_data.datetime.datetime()]
            data.append(temp)
            write_file_csv('./csv_files/comments_user.csv', columns, data)


def insert_data_comments_user(conn: psycopg2) -> None:
    with conn.cursor() as curr:
        with open('./csv_files/comments_user.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                temp = (row['user_id'], row['post_id'], row['body'], row['creation_date'])
                curr.execute('''INSERT INTO userComments (
                user_id, post_id, body, creation_date
                ) 
                VALUES (%s, %s, %s, %s)''', temp)
        conn.commit()


def add_user_in_data_base(num_users: int, conn: psycopg2) -> None:
    create_file_with_data_for_table_users(num_users)
    insert_data_from_csv_file_to_table_users(conn)


def add_post_in_data_base(num_posts: int, conn: psycopg2) -> None:
    create_file_with_data_for_table_posts(num_posts, conn)
    insert_data_all_posts_and_add_photo(conn)


def add_comment_in_data_base(num_comments: int, conn: psycopg2) -> None:
    create_file_with_data_for_table_comments_user(num_comments, conn)
    insert_data_comments_user(conn)


def get_main_information(conn: psycopg2) -> str:
    res = ''
    with conn.cursor() as curr:
        curr.execute('SELECT * FROM main_information_by_users')
        data = curr.fetchall()
        num_posts = 0
        num_comments = 0
        for row in data:
            num_posts += row[4]
            num_comments += row[5]
            res += f"ID user: {row[0]}, Numbers of posts: {row[4]}, Numbers of comments: {row[5]}," \
                   f"Name: {row[1]} {row[2]}, Password: {row[3]}\n"
        res += f"Sum users: {len(data)}, Sum posts: {num_posts}, Sum comments: {num_comments}"
    return res


if __name__ == "__main__":

    try:
        connect = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port)

        text_to_input = '''
1) Delete all data in database
2) Create all structure in database
3) Add several new users in database
4) Add several new posts in database
5) Add several new comments in database
6) Get main information from database
else) Exit
You'r choosing: '''
        while True:
            choosing = input(text_to_input)
            if choosing == '1':
                delete_all_data_from_data_base(connect)
            elif choosing == '2':
                create_all_table_in_data_base_from_file(connect)
            elif choosing == '3':
                n_users = int(input('Input numbers of new users: '))
                add_user_in_data_base(n_users, connect)
            elif choosing == '4':
                n_posts = int(input('Input numbers of new posts: '))
                add_post_in_data_base(n_posts, connect)
            elif choosing == '5':
                n_comments = int(input('Input numbers of new comments: '))
                add_comment_in_data_base(n_comments, connect)
            elif choosing == '6':
                print(get_main_information(connect))
            else:
                break
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if connect:
            connect.close()
