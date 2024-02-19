import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_oauthlib.client import OAuth
from google.cloud import firestore

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = secrets.token_hex(32)
socketio = SocketIO(app)
oauth = OAuth(app)

# Google Sign-In configuration
google = oauth.remote_app(
    'google',
    consumer_key='472730348553-gisbkr9u44bl4uif007fb7oaa24rfq32.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/plus/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Firestore setup
db = firestore.Client()

# Dummy user data for demonstration (replace with your own user data)
user_data = {'user1': '$2b$12$UEXs9PCw82tmNzF78EHci.4XbCqkX7asb1aIRsntADa2R8VDmYIEa'}

# Load chat history from Firestore
def load_chat_history_from_firestore():
    chat_ref = db.collection('chat_history')
    chat_snapshot = chat_ref.get()
    chat_history = [doc.to_dict() for doc in chat_snapshot]
    return chat_history

chat_history = load_chat_history_from_firestore()

# Routes

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], chat_history=chat_history)
    else:
        return redirect(url_for('google_login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    # ... existing login logic ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    # ... existing registration logic ...

# Google Sign-In routes
@app.route('/google/login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google/logout')
def google_logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/google/login/authorized')
def google_authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (response['access_token'], '')
    google_user = google.get('people/me')
    
    # Use the Google user's information for authentication
    # You may want to customize this based on your application's requirements
    user_info = {
        'username': google_user.data['displayName'],
        'email': google_user.data['emails'][0]['value'],
    }

    # Check if the user is already registered
    if user_info['email'] not in user_data:
        # You may want to customize the registration process based on your requirements
        user_data[user_info['email']] = bcrypt.generate_password_hash(secrets.token_hex(32)).decode('utf-8')

    # Log in the user
    session['username'] = user_info['email']

    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# SocketIO functionality

@socketio.on('message')
def handle_message(msg):
    if 'username' in session:
        print(f'{session["username"]}: {msg}')
        message = {'username': session['username'], 'message': msg}
        chat_history.append(message)
        save_message_to_firestore(message)
        socketio.emit('message', message)

def save_message_to_firestore(message):
    chat_ref = db.collection('chat_history')
    chat_ref.add(message)

if __name__ == '__main__':
    socketio.run(app, debug=True)
