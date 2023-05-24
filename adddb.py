import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-d8428-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition-d8428.appspot.com"
})

ref = db.reference('Students')

def database(data):
    print('in database:\n', data)
    for key, value in data.items():
        ref.child(key).set(value)

