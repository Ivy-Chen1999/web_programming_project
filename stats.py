from db import db
from sqlalchemy import text

def get_trainee_stats(trainee_id):
   
    
    summary_sql = text("""SELECT 
                         COUNT(*) AS total_courses,
                         SUM(CASE WHEN p.completed THEN 1 ELSE 0 END) AS completed_courses,
                         COALESCE(ROUND(SUM(CASE WHEN p.completed THEN 1.0 ELSE 0 END)  / COUNT(*) * 100, 2),0) AS completion_rate
                     FROM participation p
                     WHERE p.trainee_id = :trainee_id""")
    summary = db.session.execute(summary_sql, {"trainee_id": trainee_id}).fetchone()

   
    details_sql = text("""SELECT a.name AS activity_name, 
                            p.completed
                     FROM participation p
                     LEFT JOIN activities a ON p.activity_id = a.id
                     WHERE p.trainee_id = :trainee_id
                     ORDER BY a.name""")
    details = db.session.execute(details_sql, {"trainee_id": trainee_id}).fetchall()

    return {
        "summary": {
            "total_courses": summary.total_courses,
            "completed_courses": summary.completed_courses,
            "completion_rate": summary.completion_rate
        },
        "details": [
            {"activity_name": row.activity_name, "completed": row.completed} for row in details
        ]
    }


def get_coach_stats(coach_id):
    
    sql = text("""SELECT 
                 a.id AS activity_id,
                 a.name AS activity_name,
                 COUNT(p.id) AS total_participants,
                 SUM(CASE WHEN p.completed THEN 1 ELSE 0 END) AS completed_count,
                 COALESCE(ROUND(SUM(CASE WHEN p.completed THEN 1.0 ELSE 0 END) / NULLIF(COUNT(p.id), 0) * 100, 2), 0) AS completion_rate,
                 COALESCE(AVG(r.stars), 0) AS average_rating
             FROM activities a
             LEFT JOIN participation p ON a.id = p.activity_id
             LEFT JOIN trainee_reviews r ON a.id = r.activity_id
             WHERE a.coach_id = :coach_id
             GROUP BY a.id, a.name
             ORDER BY a.name""")
    return db.session.execute(sql, {"coach_id": coach_id}).fetchall()
