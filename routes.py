from app import app
from flask import render_template, request, redirect,flash
from datetime import datetime
import activity
import stats
import users


@app.route("/")
def index():
    logged_in = users.is_logged_in() 
    user_role = users.user_role() if logged_in else 0
    return render_template("index.html", activities=activity.get_all_activities(),logged_in=logged_in,user_role=user_role)

@app.route("/add", methods=["GET", "POST"])
def add_activity():
    users.require_role(2)

    if request.method == "GET":
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        return render_template("add_activity.html", current_time = current_time)
    
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            flash("Course name should be 1-50 characters")
            return redirect(request.referrer)
        description = request.form["description"]
        time = request.form["time"]

        coach_id = users.user_id()
        activity.add_activity(name, description, time, coach_id)
        flash("Course added successfully!", "success")
        return redirect("/")
    
@app.route("/remove", methods=["GET", "POST"])
def remove_activity():
    users.require_role(2)

    if request.method == "GET":
        my_activities = activity.get_my_activities(users.user_id())
        return render_template("remove_activity.html", activities=my_activities)
    if request.method == "POST":
        users.check_csrf()

        if "activity_id" in request.form:
            activity_id = request.form["activity_id"]
            
            activity.remove_activity(activity_id, users.user_id())
            flash("Course successfully deleted!", "success")
            
        return redirect("/")
    

@app.route("/activity/<int:activity_id>")
def show_activity(activity_id):
    if not users.is_logged_in():
        flash("Please log in to view activity details.", "error")
        return redirect("/login")
    info = activity.get_activity_info(activity_id)
    if not info:
        raise ValueError("The requested activity does not exist.")
    participation = activity.get_participation(activity_id)
    reviews = activity.get_reviews(activity_id)

    feedback = None
    if users.user_role() == 1:  
        feedback = activity.get_my_feedback(activity_id, users.user_id()) 

    return render_template("activity.html", info=info, participation=participation, \
                           reviews=reviews,feedback=feedback,hide_login_register=True)

@app.route("/join", methods=["POST"])
def join_activity():
    users.require_role(1)  
    users.check_csrf()

    activity_id = request.form["activity_id"]
    if not activity_id or not activity_id.isdigit():
        raise ValueError("Invalid activity ID.")
    activity_id = int(activity_id)
    trainee_id = users.user_id()
    activity.join_activity(int(activity_id), trainee_id)
    flash("Successfully joined the activity!", "success")

    return redirect(f"/activity/{activity_id}") 


@app.route("/complete", methods=["POST"])
def mark_as_completed():
    users.require_role(1)
    users.check_csrf()

    activity_id = request.form["activity_id"]
    activity.mark_as_completed(activity_id, users.user_id())

    flash("Activity marked as completed successfully!", "success")
    return redirect(f"/activity/{activity_id}")

@app.route("/review", methods=["POST"])
def add_review():
    users.require_role(1)
    users.check_csrf()

    activity_id = request.form["activity_id"]

    stars = int(request.form["stars"])
    if not 1 <= stars <= 5:
        flash("Invalid rating. Please enter a number between 1 and 5")
        return redirect(request.referrer)

    comment = request.form["comment"]
    if len(comment) > 1000:
        flash("Review comment is too long")
        return redirect(request.referrer)

    activity.add_review(activity_id, users.user_id(), stars, comment)
    flash("Review added successfully!", "success")
    return redirect(f"/activity/{activity_id}")

@app.route("/feedback", methods=["POST"])
def add_feedback():
    users.require_role(2) 
    users.check_csrf()  

    activity_id = request.form["activity_id"]
    trainee_id = request.form["trainee_id"]
    feedback = request.form["feedback"]

    
    if feedback.strip() == "":
        flash("Feedback cannot be null")
        return redirect(request.referrer)
    
    if not activity_id or not trainee_id or not feedback:
        flash("All fields are required.", "error")
        return redirect(request.referrer)

    coach_id = users.user_id()
    activity.add_feedback(activity_id, coach_id, trainee_id, feedback)
    flash("Feedback added successfully!", "success")
    return redirect(f"/activity/{activity_id}")


@app.route("/stats/trainee")
def trainee_stats():
    users.require_role(1)
    trainee_id = users.user_id()
    stats_data = stats.get_trainee_stats(trainee_id)
    return render_template("trainee_stats.html", 
                           summary=stats_data["summary"], 
                           participation=stats_data["details"],hide_login_register=True)


@app.route("/stats/coach")
def coach_stats():
    users.require_role(2)

    stats_data = stats.get_coach_stats(users.user_id())
    return render_template("coach_stats.html", stats=stats_data,hide_login_register=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            flash("Wrong username or password")
            return redirect(request.referrer)
        
        flash("Login successful!", "success")
        return redirect("/")
    
@app.route("/logout", methods=["GET"])
def logout():
    users.logout()
    flash("Logged out successfully!", "success")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            flash("Username should be 1-20 characters")
            return redirect(request.referrer)

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Passwords do not match")
            return redirect(request.referrer)
        if password1 == "":
            flash("Password cannot be null")
            return redirect(request.referrer)


        role = request.form["role"]
        if role not in ("1", "2"):
            flash("Invalid role")
            return redirect(request.referrer)

        if not users.register(username, password1, role):
            flash("Registration failed, please try again")
            return redirect(request.referrer)
        
        flash("Registration successful!", "success")
        return redirect("/login")
    

@app.errorhandler(ValueError)
def handle_value_error(error):
    flash(str(error), "error")  
    if not request.referrer:  
        return redirect("/")
    return redirect(request.referrer) 