from random import randint
from db import db
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

def get_all_activities():
    sql = text("""SELECT a.id, a.name, a.time, u.name AS coach_name
             FROM activities a
             LEFT JOIN users u ON a.coach_id = u.id
             WHERE a.coach_id IS NOT NULL 
             ORDER BY a.time DESC""")
    return db.session.execute(sql).fetchall()

def get_activity_info(activity_id): 
    sql = text("""SELECT a.id, a.name, a.description, a.time, u.name AS coach_name
             FROM activities a
             LEFT JOIN users u ON a.coach_id = u.id
             WHERE a.id = :activity_id""")
    return db.session.execute(sql, {"activity_id": activity_id}).fetchone()

# This is for coach. 
def get_my_activities(coach_id): 
    sql = text("""SELECT id, name, time FROM activities
             WHERE coach_id = :coach_id 
             ORDER BY time""")
    return db.session.execute(sql, {"coach_id": coach_id}).fetchall()

def add_activity(name, description, time, coach_id):
    sql = text("""INSERT INTO activities (name, description, time, coach_id)
             VALUES (:name, :description, :time, :coach_id)""")
    db.session.execute(sql, {
        "name": name,
        "description": description,
        "time": time,
        "coach_id": coach_id
    })
    db.session.commit()

def remove_activity(activity_id, coach_id):
    if not check_activity_exists(activity_id) or not check_coach_permission(activity_id, coach_id):
        return False
    sql = text("""DELETE FROM activities
             WHERE id = :activity_id AND coach_id = :coach_id""")
    result = db.session.execute(sql, {"activity_id": activity_id, "coach_id": coach_id})
    db.session.commit()
    return True
    
def join_activity(activity_id, trainee_id):
    if not check_activity_exists(activity_id) or check_participation(activity_id, trainee_id):
        return False
    
    sql = text("""INSERT INTO participation (trainee_id, activity_id, joined_at, completed)
             VALUES (:trainee_id, :activity_id, NOW(), FALSE)""")
    db.session.execute(sql, {"trainee_id": trainee_id, "activity_id": activity_id})
    db.session.commit()
    return True
    

def get_participation(activity_id): 
    sql = text("""
        SELECT u.id,u.name, 
               p.completed, 
               p.joined_at, 
               COUNT(*) OVER() AS total_participants
        FROM participation p
        JOIN users u ON p.trainee_id = u.id
        WHERE p.activity_id = :activity_id 
        ORDER BY p.joined_at
    """)
    return db.session.execute(sql, {"activity_id": activity_id}).fetchall()

# This is for trainee.
def get_my_participation(trainee_id):
    sql =text("""SELECT a.name, a.time, p.completed
             FROM participation p
             JOIN activities a ON p.activity_id = a.id
             WHERE p.trainee_id = :trainee_id 
             ORDER BY a.time""")
    return db.session.execute(sql, {"trainee_id": trainee_id}).fetchall()

def mark_as_completed(activity_id, trainee_id):
    if not check_activity_exists(activity_id) or not check_participation(activity_id, trainee_id):
        return False
    
    sql = text("""UPDATE participation 
             SET completed = TRUE 
             WHERE activity_id = :activity_id AND trainee_id = :trainee_id""")
    db.session.execute(sql, {"activity_id": activity_id, "trainee_id": trainee_id})
    db.session.commit()
    return True

def add_review(activity_id, trainee_id, stars, comment): 
    if not check_activity_exists(activity_id) or not check_participation(activity_id, trainee_id):
        return False

    try:
        sql = text("""INSERT INTO trainee_reviews (activity_id, trainee_id, stars, comment)
                VALUES (:activity_id, :trainee_id, :stars, :comment)""")
        db.session.execute(sql, {
            "activity_id": activity_id,
            "trainee_id": trainee_id,
            "stars": stars,
            "comment": comment
        })
        db.session.commit()
        return True
    except IntegrityError:
        return False

def get_reviews(activity_id): 
    sql = text("""SELECT u.name AS trainee_name, r.stars, r.comment
             FROM trainee_reviews r
             JOIN users u ON r.trainee_id = u.id
             WHERE r.activity_id = :activity_id 
             ORDER BY r.id""")
    return db.session.execute(sql, {"activity_id": activity_id}).fetchall()

def add_feedback(activity_id, coach_id, trainee_id, feedback): 
    if not check_activity_exists(activity_id) or not check_participation(activity_id, trainee_id):
        return False
    if not check_coach_permission(activity_id, coach_id):
        return False  
    
    sql = text("""INSERT INTO coach_feedback (activity_id, coach_id, trainee_id, feedback)
             VALUES (:activity_id, :coach_id, :trainee_id, :feedback)""")
    db.session.execute(sql, {
        "activity_id": activity_id,
        "coach_id": coach_id,
        "trainee_id": trainee_id,
        "feedback": feedback
    })
    db.session.commit()
    return True


def get_my_feedback(activity_id, trainee_id):
    
    sql = text("""SELECT f.feedback
             FROM coach_feedback f
             WHERE f.activity_id = :activity_id AND f.trainee_id = :trainee_id""")
    results = db.session.execute(sql, {"activity_id": activity_id, "trainee_id": trainee_id}).fetchall()
    return [{"feedback": row.feedback.strip()} for row in results if row.feedback and row.feedback.strip()]

def check_activity_exists(activity_id):
    sql = text("""SELECT id FROM activities WHERE id = :activity_id""")
    return db.session.execute(sql, {"activity_id": activity_id}).fetchone()
        

def check_coach_permission(activity_id, coach_id):
    sql = text("""SELECT id FROM activities WHERE id = :activity_id AND coach_id = :coach_id""")
    return db.session.execute(sql, {"activity_id": activity_id, "coach_id": coach_id}).fetchone()
    

def check_participation(activity_id, trainee_id):
    sql = text("""SELECT id FROM participation 
             WHERE activity_id = :activity_id AND trainee_id = :trainee_id""")
    return db.session.execute(sql, {"activity_id": activity_id, "trainee_id": trainee_id}).fetchone()


