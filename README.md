# Fitness application

This application is designed to help fitness enthusiasts manage and track their fitness progress.\
Users can engage in a variety of fitness activities, log their progress, and receive feedback from coaches.

## Users: 

The application supports two user roles:\
Trainee: Individuals who participate in fitness activities.\
Coach: Professionals who organize and manage activities and provide guidance.


## Key Features:
● Traniee can view the list of fitness activities and its detailed information(course name,description and time).

● Traniee can join fitness activities and log her/his completed trainings.

● Traniee can see the statistics of her/his progress and the feedbacks from the coaches.

● Traniee can give an comment of the fitness activity and read reviews from others.

● Coach can manage (view,set up, modify and delete) fitness activities, giving guides and instructions on the activity. 

● Coach can view the statistics of traniee's participation and summary of the courses offered by her/himself.

● Coach can give personalized feedback based on the traniee's technique.


## Current Functionalities & How to Test:   

● User Management: Registration / Login / Logout\
  Test:  
  Register as Coach / Trainee by choosing the roles, then login automatically, and click the logout link;

● Activity Management: Add / Remove course (for coach); Join Activity / Mark Completion (for trainee)  
  Test:  
  If you are a Coach, you can Add course(name, description, start time) or remove the course created by yourself.\
  If you are a Trainee, you can click the course link and Join the course and marked it as completed.

● Activity Details: Course information / Participants; Provide Feedback(for coach) / Add Reviews and See Feedbacks(for trainee)  
  Test:  
  If you are a Coach, you can provide a feedback for a specific trainee if they enrolled in the activity.
  If you are a Trainee, you can rate the activity and add reviews after joined the activity, and recieve feedback from the coach.

● Statistics: Trainee Stats / Coach Stats  
  Test:  
  If you are a Coach, you can click the stats link on the homepage and see Total participants / Completion rates /
Average ratings of the courses you provide.\
  If you are a Trainee, you can view the process of your fitness activity(number of activities joined and completion rate)



## Recent Updates
● Prevent adding activities with a start time in the past. 

● Display upcoming events at the top. 

● Add constraints for repeating usernames, password length, feedback and comment length. 

● Enable automatic login after registration and redirect to the homepage. 

● Allow trainees to submit only one review. 

● Standardize error messages and validation functions. 

● Prevent access to the login and registration pages after the user is already logged in. 

● Add CSS templates to enhance the interface.

● Utilize pylint to polish the code 


## Local Deployment

● Set Up Environment Variables，Create a .env file in the root folder and specify its content:

```
DATABASE_URL=<your-local-database-url>
SECRET_KEY=<your-secret-key>
```
● Activate a virtual environment and install the required modules:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
● Set Up the Database：
```
$ psql < schema.sql
```
● Run the Application：
```
$ flask run
```









