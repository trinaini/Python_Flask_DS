from queue import Queue
from flask import Flask, json, jsonify, request
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy  import SQLAlchemy
import random

import linked_list
import hashtable
import binary_search_tree 
import queue
import stack

app = Flask(__name__)

# configuration to use local file as database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

## configuring sqlite3 to enforce foreign key contraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

## create instance to database
db = SQLAlchemy(app)
now = datetime.now()

## models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade = "all, delete") # relationship to another table "Blog post"

class BlogPost(db.Model):
    __tablename__="blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    

## routes
@app.route("/user", methods = ["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"],
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 200

@app.route("/user/descending_id", methods = ["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    # adding in the beginning will return users in descending order
    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/ascending_id", methods = ["GET"])
def get_all_users_ascending():
    users = User.query.all() 
    all_users_ll = linked_list.LinkedList()

    #adding at the end of linked list will return users in ascending order

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/<user_id>", methods = ["GET"])
def get_user(user_id):
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    
    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200

@app.route("/user/<user_id>", methods = ["DELETE"])
def delete_user(user_id):

    user = User.query.filter_by(id = user_id).first()

    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route("/blog_post/<user_id>", methods = ["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    user = User.query.filter_by(id = user_id).first()

    if not user:
        return jsonify({"message": "user does not exist!"}), 400

    ht = hashtable.HashTable(10)

    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    # ht.print_hash_table()

    blog_post = BlogPost(
        title = ht.get_value("title"),
        body = ht.get_value("body"),
        date = ht.get_value("date"),
        user_id = ht.get_value("user_id")
    )

    db.session.add(blog_post)
    db.session.commit()
    return jsonify({"message": "new blog post created"}), 200

@app.route("/blog_post/<blog_post_id>", methods = ["GET"])
def get_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.Binary_Search_Tree()
    for post in blog_posts:

        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"}), 400

    return jsonify(post)
    
@app.route("/blog_post/numeric_body", methods = ["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()

    q = queue.Queue()

    for post in blog_posts:
        q.enqueue(post)

    return_list = []

    for i in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append(
            {
                "id": post.data.id,
                "title": post.data.title,
                "body": post.data.body,
                "user_id": post.data.user_id,
            }
        )
        
        return jsonify(return_list)

@app.route("/blog_post/delete_last_10", methods = ["DELETE"])
def delete_blog_post():
    blog_posts = BlogPost.query.all()

    s = stack.Stack()

    for post in blog_posts:
        s.push(post)


    for i in range(10):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data)
        db.session.commit()

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug = True)

