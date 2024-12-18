import os
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db import db

def login(name, password):
    sql = text("SELECT password, id, role FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False

    session["user_id"] = user[1]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True


def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(name, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (name, password, role)
                 VALUES (:name, :password, :role)""")
        db.session.execute(sql, {"name": name, "password": hash_value, "role": role})
        db.session.commit()
        return login(name, password)
    except IntegrityError:
        return "duplicate"
    except Exception:
        return False

def user_id():
    return session.get("user_id", 0)

def user_role():
    return session.get("user_role", 0)


def is_logged_in():
    return "user_id" in session


def require_role(role):
    if session.get("user_role", 0) != role:
        abort(403, description="You do not have sufficient permissions.")

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
