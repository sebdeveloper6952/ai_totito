import socketio

# constants
USERNAME = "SebasArriola"
TOURNAMENT_ID = 1000
USER_ROLE = "player"
SERVER_URL = "http://3.12.129.126:4000"

# global client
client = socketio.Client()

# sign in to the server using constants above
def sign_in():
    client.emit('signin', {
        'user_name': USERNAME,
        'tournament_id': TOURNAMENT_ID,
        'user_role': USER_ROLE
    })

# server events
@client.event
def connect():
    print("Connected to server!")
    sign_in()

@client.event
def disconnect():
    print("Connection to server closed!")

@client.event
def ok_signin():
    print("Sign in succesful!")

@client.event
def ready(data):
    print(data)

# main program
client.connect(SERVER_URL)