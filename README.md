# triton-web-messenger-app
Web Messenger Application in Python using Flask, deployed on GAE. This is an instant messaging app with user registration, login, and Google Sign-In functionality.

Project Overview:

Basic App Structure:
Created a basic Flask project structure with templates, static files, and a main app.py file.
Used Flask-SocketIO for real-time communication.

User Registration and Login:
Implemented user registration and login functionality.
Stored user credentials securely using Flask-Bcrypt for password hashing.

Google Sign-In Integration:
Integrated Google Sign-In using Flask-OAuthlib for authentication.
Allowed users to sign in with their Google accounts.

Persistent Chat History:
Stored and retrieved chat history using Google Cloud Firestore.

Deployment to Google App Engine:
Deployed the Flask app to Google App Engine.
Configured the app.yaml file for App Engine deployment.

Testing:
Set up basic test cases using pytest and Flask-Testing.
Checked code coverage using pytest-cov.

Local Development:
Ensured the ability to run the application locally for development and testing.

Key Files and Components:
app.py:
Main application file containing the Flask app, SocketIO configuration, and routes.
Includes user registration, login, Google Sign-In, and real-time chat functionality.

templates/:
Folder containing HTML templates for the application, including index.html, login.html, and register.html.

static/:
Folder containing static files such as CSS stylesheets (style.css).

requirements.txt:
File specifying the required Python packages for the application.

pytest.ini:
Configuration file for pytest with coverage options.

tests/ (Folder):
Folder containing test cases (test_app.py) for the application.

Deployment Steps:

Google Cloud Setup:
Created a Google Cloud project.
Enabled the App Engine API.
Set up Firestore for chat history.

Google App Engine Deployment:

Configured the app.yaml file for App Engine.
Deployed the Flask app to Google App Engine.

Testing Steps:

Test Setup:
Installed testing libraries (pytest, Flask-Testing).
Configured pytest.ini for coverage reporting.

Test Cases:
Created basic test cases in the tests/ folder (test_app.py).
Ran tests using the pytest command.

Local Development:
Local Run:
Ran the Flask app locally for development using the Flask development server.
Configured SocketIO to run locally.

Access Locally Deployed App:
Accessed the locally running application at http://localhost:5000.

Ongoing Considerations:

Maintenance:
Ongoing maintenance and updates to the application code as needed.
Continuous testing and improvement of test coverage.

Security:
Regularly reviewed and enhanced security measures, such as secure handling of secrets and sensitive information.
