This was our final project for our Software Engineering class. This was created in a hurry, starting with almost no knowledge of Web Development, so expect some unorthodox methods inside this codebase!

Demo: https://www.youtube.com/watch?v=zSRkpmQ3SuI

# Chat-Application
 
The LeeBRA Chat Application able to run through a web server with an address accessible through the internet. The system check authentication by checking if their username and passwords match the SQL user data, which stored in the web server. The system runs on Python code using the Flask Web Framework. Also using JavaScript and HTML for interactive web-pages that will update to user events, such as received messages, friend requests, etc.

# Description of services that the software offers: 
(Completed features from Requirement Specification Document) 
1.	The Initial Chat application screen shall have the LeeBRA logo, a username box, a password box, as well as “Forgot Password”, “Register”, and “FAQ” buttons.

2.	The user shall be able to register an account with a username and password combo.
2.1.	The username must be between 4 and 14 characters long and may only contain letters and numbers.
2.2.	The password must be at least 5 characters long and must contain at least one letter, one number, and one special character: !@#$%^&*-+().
2.3.	The user shall be prompted to choose a security question from a selection of 5, then they must answer it.
2.4.	During registration, if the username is already in the database, the error message “Username Taken” shall be displayed.
2.5.	The user shall be warned to save their username, password, and security words since if forgotten, their account will be inaccessible.

3.	The user shall be able to log in using a username and password combo.
3.1.	Only a matching username and password combo shall grant the access to the account.
3.2.	There shall be a “Forgot Password” option on the login page. 
3.2.1.	Upon selecting “Forgot Password”, the user shall be prompted to enter his/her username. 
3.2.2.	If the username does not match anyone in the database, an error message will display “User not found”
3.2.3.	If the username matches the name in the database, the user will be prompted to answer their security question.
3.2.4.	If the answer is successful, the application shall prompt the user to change their password. After that the user must enter their username and new password to gain access to the account.
3.2.5.	If the answer is wrong, the message shall prompt “Incorrect answer”

4.	The user shall have access to many features once logged in. 
4.1.	The “Log out” button shall be available while the user is logged in.
4.2.	A search box shall be available while the user is logged in to find other users in the database.
4.3.	The “Block This User” button shall be available while the user logged in to prevent users from messaging them.
4.4.	A “Block List” button shall be available while the user is logged in to display on request accounts which the user does not want to receive messages from.
4.5.	“FAQ“ button shall be available while the user logged in to help users with possible issues or questions.


5.	The user shall be able to log out of their account with the press of a button.
5.1.	Once logged out, the user shall only be able to view the initial Chat Application  screen.

6.	The user shall be able to send textual messages.
6.1.	The application shall play a different sound when sending a message.
6.2.	Every message shall have information of the username who created the message and date and time of creation in format (MM:DD:YYYY,  HH:MM:SS,  time 24 hour format).
6.3.	All messages in the chat application shall be displayed in date-time order by most recent.
6.4.	All messages in the chat application shall be available immediately.

7.	The user shall be able to search for other users by username in order to message them. 
7.1.	The user shall be able to input letter/digit characters to begin the search. The results will only include those which include a part that exactly matches the inputted characters. For example, if the user inputs “dog”, they shall see results like “theDogMan200”, “dog”, and “dogFrog”, but shall not see results like “theGodMan200”
8.	The user shall be able to add users to a “Block List”, preventing them from sending him/her  any messages.
8.1.	The user shall be able to access his/her block list and remove users from it.

9.	The user shall be able to delete messages.
9.1.	The user shall be able to delete messages one at a time 

10.	The user shall be able to message multiple users at once in a “Group Chat”.
10.1.	Any registered user shall be able to create group chat.
10.2.	The group chat shall prompt the user to set a name upon creation.
10.3.	Each group chat user shall have certain privileges.
10.3.1.	The user shall be able to add members to the chat.
10.3.2.	The user shall be able to edit the group name.
10.3.3.	The user shall be able to leave the group.

11.	The user shall be able to change the color of their messages.
11.1.	The user shall be able to change background message color.
11.2.	The user shall be able to change text color.
11.3.	There shall be at least 5 colors to choose from.
11.4.	The user shall be able to choose between smaller and larger text sizes.
11.5.	The user shall not be able to change their message font.


12.	 Users shall be able to set a profile picture to help identify themselves.
12.1.	Only PNG or JPG file types shall be acceptable images
12.2.	Upon uploading a picture, the user shall be prompted to crop it to be a circle.

13.	There shall be a customizable “user status” so users can update others on what they’re doing.
13.1.	The user status must be between 4 and 80 characters long and may contain letters, numbers, and special characters: !@#$%^&*-+().
13.2.	Each user’s status shall be viewable by selecting that user’s profile picture anywhere in the application.

# Deployment: 
Team used the web host PythonAnywhere.com for the Chat Application. To access the deployment environment, developer must login to the LeeBRA PythonAnywhere account. 
Chat application available at leebra.pythonanywhere.com
