# Fitness application

This application can manage and record fitness progress for Fitness enthusiasts.
## Users: 
Traniee and Coach. Each user can register as either a trainee or a coach. \
Users can log in, log out, and create new accounts.

## Key Features:
● Traniee can view the list of fitness activities and its detailed information(course name,description and time).

● Traniee can join fitness activities and log her/his completed trainings.

● Traniee can see the statistics of her/his progress and the feedbacks from the coaches.

● Traniee can give an comment of the fitness activity and read reviews from others.

● Coach can manage (view,set up, modify and delete) fitness activities, giving guides and instructions on the activity. 

● Coach can see the statistics of traniee's participation and each traniee's completed trainings.

● Coach can give personalized feedback based on the traniee's technique.


## Current Function & How to Test:  
please use the following modules in requirements.txt  

● User Management: Registration / Login / Logout\
  Test:  
  Register as Coach / Trainee by choosing the roles, then login, and click the logout link;

● Activity Management: Add / Remove course (for coach); Join Activity / Mark Completion (for trainee)  
Test:  
  If you are a Coach, you can Add course(name, description, start time) or remove the course created by yourself.\
  If you are a Trainee, you can click the course link and Join the course and marked it as completed.

● Activity Details: Course information / Participants; Provide Feedback(for coach) / Add Reviews and See Feedbacks(for trainee)  
  Test:  
  If you are a Coach, you can provide a feedback for a specific trainee if they enrolled in the activity.
  If you are a Trainee, you can rate the activity and add reviews, and see feedback from the coach.

● Statistics: Trainee Stats / Coach Stats  
  Test:  
  If you are a Coach, you can click the stats link on the homepage and see Total participants / Completion rates /
Average ratings of the courses you provide.\
  If you are a Trainee, you can view the process of your fitness activity(number of activities joined and completion rate)

## Current Update
● Prevent adding activities with a start time in the past. 

● Display upcoming events at the top. 

● Add constraints for repeating usernames, password length, feedback and comment length. 

● Enable automatic login after registration and redirect to the homepage. 

● Allow trainees to submit only one review. 

● Standardize error messages and validation functions. 

● Prevent access to the login and registration pages after the user is already logged in. 

● Add CSS templates to enhance the interface.


## Future Work:
● Utilize pylint to polish the code 

● Maybe use Bootstrap for better UI





