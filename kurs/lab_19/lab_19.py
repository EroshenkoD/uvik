"""NoSQL Blog
Create the db to store your blog posts using Mongo.

In this task you need:

create the db, collection and documents
insert objects
retrieve all objects and object via filtering
update at least 1 object
delete at least 1 object
"""
import datetime
import pprint
from mimesis import Generic
from pymongo import MongoClient
from random import randint

NAME_DB = 'blog'
NAME_COLLECTION = 'messages'


def delete_database(name_bd: str) -> str:
    client.drop_database(name_bd)
    return 'Database deleted'


def insert_messages_in_database(name_db: str, name_collection: str, num_messages: int) -> object:
    insert_data = []
    for i in range(num_messages):
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M:%S")
        random_data = Generic('en')
        temp_mess = {
            "id_post": i,
            "body": random_data.text.title(),
            "author": random_data.person.first_name(),
            "creation_datetime": now
        }
        insert_data.append(temp_mess)
    return client[name_db][name_collection].insert_many(insert_data)


def get_all_messages(name_db: str, name_collection: str) -> object:
    return client[name_db][name_collection].find()


def get_last_messages(name_db: str, name_collection: str, num_messages: int) -> object:
    return client[name_db][name_collection].find().sort('creation_datetime', -1).limit(num_messages)


def get_num_messages_group_by_id_posts(name_db: str, name_collection: str) -> object:
    return client[name_db][name_collection].aggregate([{"$group": {"_id": "$id_post", "num_mess": {"$sum": 1}}}])


def get_len_body_of_message(name_db: str, name_collection: str) -> object:
    return client[name_db][name_collection].aggregate([{'$project': {'author': 1, 'length': {'$strLenCP': "$body"}}}])


def change_some_message(name_db: str, name_collection: str) -> object:
    list_id_message = client[name_db][name_collection].find({'body': {'$ne': 'CHANGE BODY'}}).distinct('_id')
    if list_id_message:
        id_change_message = list_id_message[randint(0, len(list_id_message) - 1)]
        return client[name_db][name_collection].update_one({'_id': id_change_message},
                                                           {'$set': {'body': 'CHANGE BODY'}})


def delete_some_message(name_db: str, name_collection: str) -> object:
    list_id_message = client[name_db][name_collection].find().distinct('_id')
    if list_id_message:
        id_change_message = list_id_message[randint(0, len(list_id_message) - 1)]
        return client[name_db][name_collection].delete_one({'_id': id_change_message})


if __name__ == "__main__":
    with MongoClient() as client:
        while True:
            text_to_input = '''
1) Delete database
2) Add several new messages
3) Delete random message
4) Change body of random message
5) Get all data
6) Get several last messages
7) Get number of messages group by ID post
8) Get len body of messages
else) Exit
You'r choosing: '''
            choosing = input(text_to_input)
            if choosing == '1':
                print(delete_database(NAME_DB))
            elif choosing == '2':
                n_mess = int(input('Input numbers of new messages: '))
                res = insert_messages_in_database(NAME_DB, NAME_COLLECTION, n_mess)
                print(res.acknowledged)
            elif choosing == '3':
                res = delete_some_message(NAME_DB, NAME_COLLECTION)
                print(res.acknowledged)
            elif choosing == '4':
                res = change_some_message(NAME_DB, NAME_COLLECTION)
                print(res.raw_result)
            elif choosing == '5':
                temp = get_all_messages(NAME_DB, NAME_COLLECTION)
                for i in temp:
                    pprint.pprint(i)
            elif choosing == '6':
                n_mess = int(input('Input numbers of new messages: '))
                temp = get_last_messages(NAME_DB, NAME_COLLECTION, n_mess)
                for i in temp:
                    pprint.pprint(i)
            elif choosing == '7':
                temp = get_num_messages_group_by_id_posts(NAME_DB, NAME_COLLECTION)
                for i in temp:
                    pprint.pprint(i)
            elif choosing == '8':
                temp = get_len_body_of_message(NAME_DB, NAME_COLLECTION)
                for i in temp:
                    pprint.pprint(i)
            else:
                break

