import  firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate()
firebase_admin.initialize(cred)